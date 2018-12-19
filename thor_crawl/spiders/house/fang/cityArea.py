"""
搜房网-所有城市
增量爬取
该爬虫，一般情况只需要爬取一次就够了：因为中国的城市变化，个人觉得是不频繁的
http://www.fang.com/SoufunFamily.htm
"""
import re

import scrapy
from scrapy import Selector
from scrapy.spiders import Spider

from thor_crawl.spiders.spider_setting import DEFAULT_DB_ENV
from thor_crawl.utils.commonUtil import CommonUtil
from thor_crawl.utils.db.daoUtil import DaoUtils


class CityArea(Spider):
    name = 'community_fang_city_area'
    handle_httpstatus_list = [302, 204, 206, 404, 500]

    start_urls = ['http://www.fang.com/SoufunFamily.htm']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ============ 工具 ============
        self.dao = DEFAULT_DB_ENV
        self.common_util = CommonUtil()

        # ============ 数据库中已存在的数据 ============
        self.db_data = set()
        self.temp = self.dao.get_all('SELECT area_url FROM fang_city_area')
        for row in self.temp:
            self.db_data.add(row['area_url'])

        # ============ 持久化相关变量定义 ============
        self.save_threshold = 10  # 一次性插入数据库阈值
        self.persistent_data = list()  # 内存暂存处理的数据，批量插入数据库
        self.main_table = 'fang_city_area'  # 数据库存储表

        # ============ 业务 ============
        self.no_zxq = 'http://esf.{city_code}.fang.com/housing/'

    def __del__(self):
        self.save_final()

    def closed(self, res):
        self.save_final()

    def parse(self, response):
        try:
            body = response.body.decode('gb18030').encode('utf-8')
        except UnicodeDecodeError as e:
            print(e)
            body = response.body
        meta = response.meta
        hxf = Selector(text=body)

        trs = hxf.xpath('//div[@id="c02"]/table/tr')  # 获取所有的行数据
        last_province = '未知'

        for tr in trs[:-1]:
            province_name = self.common_util.get_extract(tr.xpath('td[2]/strong/text()'))  # 获取省份名称文本值
            last_province = last_province if province_name is None or province_name == '' else province_name  # 为空的话取之前的省份名称
            meta['province_name'] = last_province  # 省份名称放入meta，带到下一级使用

            cities = tr.xpath('td[3]/a')  # 获取所有的城市列表
            for city in cities:
                city_name = self.common_util.get_extract(city.xpath('text()'))  # 获取城市名称文本值
                city_index_url = self.common_util.get_extract(city.xpath('@href'))  # 获取城市首页链接

                meta['city_name'] = city_name
                meta['city_index_url'] = city_index_url
                meta['city_code'] = re.search(r'http://(.+)\.fang\.com', city_index_url).group(1)  # http://hz.fang.com/

                if meta['city_code'] == 'sx':
                    meta['city_code'] = 'shaoxing'

                yield scrapy.FormRequest(url=self.no_zxq.format(city_code=meta['city_code']), method='GET', meta=meta, callback=self.parse_area)

    def parse_city_index(self, response):
        try:
            body = response.body.decode('gb18030').encode('utf-8')
        except UnicodeDecodeError as e:
            print(e)
            body = response.body
        meta = response.meta
        hxf = Selector(text=body)

        community_url = hxf.xpath('//div[@id="dsy_D01_03"]/div[@class="listBox"]/ul/li[4]/a/@href')

        if community_url is None or len(community_url) == 0:
            print('------parse_city_index, community_url is none:', meta)
        else:
            yield scrapy.FormRequest(url=self.common_util.get_extract(community_url), method='GET', meta=meta, callback=self.parse_area)

    def parse_area(self, response):
        try:
            body = response.body.decode('gb18030').encode('utf-8')
        except UnicodeDecodeError as e:
            print(e)
            body = response.body
        meta = response.meta
        url = response.url
        hxf = Selector(text=body)

        a_tag_list = hxf.xpath('//div[@class="qxName"]/a')

        print('len: ', len(a_tag_list))

        if a_tag_list is None or len(a_tag_list) <= 1:
            print('------parse_area, no area in ', meta['province_name'], meta['city_name'])
        else:
            for a_tag in a_tag_list[1:]:
                search_group = re.search(r'(.*)/housing/', url)

                if search_group is not None:
                    meta['area_name'] = self.common_util.get_extract(a_tag.xpath('text()'))
                    meta['area_url'] = self.common_util.get_extract(a_tag.xpath('@href'))
                    meta['base_url'] = search_group.group(1)
                    yield scrapy.FormRequest(url=meta['base_url'] + meta['area_url'], method='GET', meta=meta, callback=self.parse_sub)

    def parse_sub(self, response):
        try:
            body = response.body.decode('gb18030').encode('utf-8')
        except UnicodeDecodeError as e:
            print(e)
            body = response.body
        meta = response.meta
        hxf = Selector(text=body)

        a_tag_list = hxf.xpath('//p[@id="shangQuancontain"]/a')

        if a_tag_list is None or len(a_tag_list) <= 1:
            print('------parse_sub, no sub in ', meta['province_name'], meta['city_name'], meta['area_name'])
        else:
            for a_tag in a_tag_list[1:]:
                self.persistent_data.append(
                    {
                        'province_name': meta['province_name'],
                        'city_name': meta['city_name'],
                        'city_index_url': meta['city_index_url'],
                        'base_url': meta['base_url'],
                        'area_name': meta['area_name'],
                        'area_url': meta['area_url'],
                        'sub_name': self.common_util.get_extract(a_tag.xpath('text()')),
                        'sub_url': meta['base_url'] + self.common_util.get_extract(a_tag.xpath('@href')),
                    }
                )
        self.save()

    def save(self):
        if len(self.persistent_data) > self.save_threshold:
            try:
                self.dao.customizable_add_batch(self.main_table, self.persistent_data)
            except AttributeError as e:
                self.dao = DaoUtils()
                self.dao.customizable_add_batch(self.main_table, self.persistent_data)
                print('save except:', e)
            finally:
                self.persistent_data = list()

    def save_final(self):
        if len(self.persistent_data) > 0:
            try:
                self.dao.customizable_add_batch(self.main_table, self.persistent_data)
            except AttributeError as e:
                self.dao = DaoUtils()
                self.dao.customizable_add_batch(self.main_table, self.persistent_data)
                print('save_final except:', e)
            finally:
                self.persistent_data = list()
