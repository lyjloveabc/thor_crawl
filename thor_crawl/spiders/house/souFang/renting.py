"""
搜房网-租房信息
"""
import re

import scrapy
from scrapy import Selector
from scrapy.spiders import Spider

from thor_crawl.spiders.spider_setting import DEFAULT_DB_ENV
from thor_crawl.utils.commonUtil import CommonUtil
from thor_crawl.utils.db.daoUtil import DaoUtils


class Renting(Spider):
    name = 'sou_fang_renting'
    handle_httpstatus_list = [302, 204, 206, 404, 500]

    start_urls = ['http://www.souFang.com/SoufunFamily.htm']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ============ 工具 ============
        self.dao = DEFAULT_DB_ENV
        self.common_util = CommonUtil()

        # ============ 持久化相关变量定义 ============
        self.save_threshold = 20  # 一次性插入数据库阈值
        self.persistent_data = list()  # 内存暂存处理的数据，批量插入数据库
        self.main_table = 'sou_fang_renting'  # 数据库存储表

        # ============ 业务 ============
        province_name = '浙江'
        city_name = '杭州'
        self.target = 'SELECT id, province_name, city_name, city_index_url ' \
                      'FROM sou_fang_city_index ' \
                      'WHERE province_name = "{province_name}" and city_name = "{city_name}"'.format(province_name=province_name, city_name=city_name)
        self.url_template = 'http://{city_code}.zu.fang.com/'  # 租房首页的模板URL

    def __del__(self):
        self.save_final()

    def start_requests(self):
        start_requests = list()
        for row in self.dao.get_all(self.target):
            if row['city_index_url'] != '':
                meta = {
                    'city_index_id': row['id'],
                    'province_name': row['province_name'],
                    'city_name': row['city_name']
                }
                url = self.url_template.format(city_code=re.search(r'http://(.+)\.fang\.com', row['city_index_url']).group(1))
                start_requests.append(scrapy.FormRequest(url=url, method='GET', meta=meta))
        return start_requests

    def closed(self, res):
        self.save_final()

    # 拿到所有的地区，去掉"不限"
    def parse(self, response):
        try:
            body = response.body.decode('gb18030').encode('utf-8')
        except UnicodeDecodeError as e:
            print(e)
            body = response.body
        meta = response.meta
        url = response.url
        hxf = Selector(text=body)

        a_tag_list = hxf.xpath('//dl[@id="rentid_D04_01"]/dd/a')
        print('a_tag_list len: ', len(a_tag_list))

        if a_tag_list is None or len(a_tag_list) <= 1:
            print('------parse, no data in ', meta['province_name'], meta['city_name'])
        else:
            for a_tag in a_tag_list:
                meta['area_name'] = self.common_util.get_extract(a_tag.xpath('text()'))
                meta['area_url'] = self.common_util.get_extract(a_tag.xpath('@href'))
                meta['base_url'] = url

                if meta['area_name'] is not None and meta['area_name'] != '' and meta['area_name'] != '不限':
                    print(url + meta['area_url'])
                    yield scrapy.FormRequest(url=url + meta['area_url'], method='GET', meta=meta, callback=self.parse_area)

    def parse_area(self, response):
        try:
            body = response.body.decode('gb18030').encode('utf-8')
        except UnicodeDecodeError as e:
            print(e)
            body = response.body
        meta = response.meta
        url = response.url
        hxf = Selector(text=body)

        dl_tag_list = hxf.xpath('//div[@class="houseList"]/dl')
        print('dl_tag_list len: ', len(dl_tag_list))

        if dl_tag_list is None or len(dl_tag_list) <= 1:
            print('------parse_area, no data in ', meta['province_name'], meta['city_name'], meta['area_name'])
        else:
            for dl_tag in dl_tag_list:
                feature = ''
                feature_span_list = dl_tag.xpath('dd/p[5]/span')
                for feature_span in feature_span_list:
                    feature += self.common_util.get_extract(feature_span.xpath('text()')) + ','
                feature = feature[:-1] if len(feature) > 1 else feature
                self.persistent_data.append(
                    {
                        'city_index_id': meta['city_index_id'],
                        'province_name': meta['province_name'],
                        'city_name': meta['city_name'],
                        'area_name': meta['area_name'],
                        'detail_url': self.common_util.get_extract(dl_tag.xpath('dd/p[1]/a/@href')),
                        'name': self.common_util.get_extract(dl_tag.xpath('dd/p[1]/a/text()')),
                        'rent_way': self.common_util.get_extract(dl_tag.xpath('dd/p[2]/text()[1]')),
                        'door_model': self.common_util.get_extract(dl_tag.xpath('dd/p[2]/text()[2]')),
                        'area': self.common_util.get_extract(dl_tag.xpath('dd/p[2]/text()[3]')),
                        'toward': self.common_util.get_extract(dl_tag.xpath('dd/p[2]/text()[4]')),
                        'unit_price': self.common_util.get_extract(dl_tag.xpath('dd//span[@class="price"]/text()')),
                        'feature': feature
                    }
                )
        # 下一页
        page_a_list = hxf.xpath('//div[@class="fanye"]/a')
        if len(page_a_list) > 0:
            for page_a in page_a_list:
                if self.common_util.get_extract(page_a.xpath('text()')) == '下一页':
                    yield scrapy.FormRequest(
                        url=meta['base_url'] + self.common_util.get_extract(page_a.xpath('@href')), method='GET', meta=meta, callback=self.parse_area
                    )

        self.save()

    def save(self):
        if len(self.persistent_data) > self.save_threshold:
            try:
                self.dao.customizable_add_ignore_batch(self.main_table, self.persistent_data)
            except AttributeError as e:
                self.dao = DaoUtils()
                self.dao.customizable_add_ignore_batch(self.main_table, self.persistent_data)
                print('save except:', e)
            finally:
                self.persistent_data = list()

    def save_final(self):
        if len(self.persistent_data) > 0:
            try:
                self.dao.customizable_add_ignore_batch(self.main_table, self.persistent_data)
            except AttributeError as e:
                self.dao = DaoUtils()
                self.dao.customizable_add_ignore_batch(self.main_table, self.persistent_data)
                print('save_final except:', e)
            finally:
                self.persistent_data = list()
