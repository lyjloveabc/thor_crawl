# coding=utf-8
import re

import scrapy
from scrapy import Selector
from scrapy.spiders import Spider

from thor_crawl.spiders.spider_setting import DEFAULT_DB_ENV
from thor_crawl.utils.commonUtil import CommonUtil
from thor_crawl.utils.db.daoUtil import DaoUtils
from thor_crawl.utils.email.emailUtil import EmailUtils
from thor_crawl.utils.system.systemUtil import SystemUtil


class CityZone(Spider):
    name = 'fang_city_zone_2'
    handle_httpstatus_list = [204, 206, 404, 500]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ============ 工具 ============
        self.dao = DEFAULT_DB_ENV
        self.common_util = CommonUtil()

        # ============ 持久化相关变量定义 ============
        self.save_threshold = 20  # 一次性插入数据库阈值
        self.persistent_data = list()  # 内存暂存处理的数据，批量插入数据库
        self.main_table = 'fang_city_zone_new'  # 数据库存储表
        self.sleep_count = 1

        # ============ 业务数据 ============
        self.need_city = [
            '湖州',
            '衢州',
            '丽水',
            '舟山',
            '连云港',
            '淮安',
            '盐城',
            '扬州',
            '镇江',
            '泰州',
            '宿迁'
        ]
        self.sign = '/housing/'
        self.detail_sign = 'xiangqing'

        other_url = 'https://{code}.esf.fang.com'
        bj_url = 'https://esf.fang.com'
        self.cities = dict()
        with open('city_after_format.txt', 'r', encoding='utf-8') as f:
            for line in f.readlines():
                data = line.replace('\n', '')
                city_info = data.split(',')
                code = re.search(r'http://(.+)\.fang\.com', city_info[2]).group(1)
                self.cities[city_info[1]] = {
                    'province_name': city_info[0],
                    'city_name': city_info[1],
                    'city_index_url': city_info[2],
                    'city_base_url': bj_url if city_info[1] == '北京' else other_url.format(code=code),
                    # 'city_base_url': other_url.format(code=code),
                    'city_code': code
                }

    def __del__(self):
        self.save_final()
        # EmailUtils.send_mail("爬虫结束了，快回来", "1111")
        SystemUtil.say(circle_num=2)

    def closed(self, res):
        self.save_final()
        # EmailUtils.send_mail("爬虫结束了，快回来", "1111")
        SystemUtil.say(circle_num=2)

    def start_requests(self):
        start_requests = set()
        for row in self.need_city:
            if row in self.cities.keys():
                start_requests.add(scrapy.FormRequest(url=self.cities[row]['city_base_url'] + self.sign, method='GET', meta=self.cities[row]))
            else:
                print("----------------------------------no ", row)
        return start_requests

    def parse(self, response):
        try:
            body = response.body.decode('gb18030').encode('utf-8')
        except UnicodeDecodeError as e:
            print(e)
            body = response.body
        hxf = Selector(text=body)
        meta = response.meta

        areas = hxf.xpath('//div[@id="houselist_B03_02"]/div[@class="qxName"]/a')

        for area in areas[:-1]:
            meta['first_area'] = self.common_util.get_extract(area.xpath('text()'))
            href = self.common_util.get_extract(area.xpath('@href'))
            yield scrapy.FormRequest(url=meta['city_base_url'] + href, method='GET', meta=meta, callback=self.parse_first_area)

        self.save()

    def parse_first_area(self, response):
        try:
            body = response.body.decode('gb18030').encode('utf-8')
        except UnicodeDecodeError as e:
            print(e)
            body = response.body
        hxf = Selector(text=body)
        meta = response.meta

        areas = hxf.xpath('//p[@id="shangQuancontain"]/a')

        for area in areas[:-1]:
            meta['second_area'] = self.common_util.get_extract(area.xpath('text()'))
            href = self.common_util.get_extract(area.xpath('@href'))
            yield scrapy.FormRequest(url=meta['city_base_url'] + href, method='GET', meta=meta, callback=self.parse_second_area)

    def parse_second_area(self, response):
        try:
            body = response.body.decode('gb18030').encode('utf-8')
        except UnicodeDecodeError as e:
            print(e)
            body = response.body
        hxf = Selector(text=body)
        meta = response.meta

        houses = hxf.xpath('//div[@class="houseList"]/div')

        for house in houses:
            meta['name'] = self.common_util.get_extract(house.xpath('dl/dd/p/a/text()'))
            meta['url'] = self.common_util.get_extract(house.xpath('dl/dd/p/a/@href'))
            meta['price'] = self.common_util.get_extract(house.xpath('p[@class="priceAverage"]/span/text()'))
            # yield scrapy.FormRequest(url='https:' + meta['url'], method='GET', meta=meta, callback=self.parse_zone_index)

            # if self.sleep_count % 1000 == 0:
            #     print("sleep---------------5:")
            #     time.sleep(5)
            # meta['detail_url'] = str(meta['url']).replace('/esf/', '/xiangqing/') if '/esf/' in meta['url'] else (meta['url'] + 'xiangqing/')
            # yield scrapy.FormRequest(url='https:' + meta['detail_url'], method='GET', meta=meta, callback=self.parse_zone_detail)
            # self.sleep_count += 1

            meta['detail_url'] = str(meta['url']).replace('/esf/', '/xiangqing/') if '/esf/' in meta['url'] else (meta['url'] + 'xiangqing/')
            self.persistent_data.append(
                {
                    'province_name': meta['province_name'],
                    'city_name': meta['city_name'],
                    'first_area': meta['first_area'],
                    'second_area': meta['second_area'],
                    'name': meta['name'],
                    'url': meta['url'],
                    'detail_url': meta['detail_url']
                }
            )
        self.save()

        # 下一页
        page_a_list = hxf.xpath('//div[@id="houselist_B14_01"]/a')
        if len(page_a_list) > 0:
            for page_a in page_a_list:
                if self.common_util.get_extract(page_a.xpath('text()')) == '下一页':
                    yield scrapy.FormRequest(
                        url=meta['city_base_url'] + self.common_util.get_extract(page_a.xpath('@href')), method='GET', meta=meta, callback=self.parse_second_area
                    )

    def parse_zone_index(self, response):
        try:
            body = response.body.decode('gb18030').encode('utf-8')
        except UnicodeDecodeError as e:
            print(e)
            body = response.body
        hxf = Selector(text=body)
        meta = response.meta

        meta['detail_url'] = self.common_util.get_extract(hxf.xpath('//li[@data="xqxq"]/a/@href'))
        yield scrapy.FormRequest(url='https:' + meta['detail_url'], method='GET', meta=meta, callback=self.parse_zone_detail)

    def parse_zone_detail(self, response):
        try:
            body = response.body.decode('gb18030').encode('utf-8')
        except UnicodeDecodeError as e:
            print(e)
            body = response.body
        hxf = Selector(text=body)
        meta = response.meta

        land_area = ''
        building_area = ''
        property_fee = ''
        fields = hxf.xpath('//dl[@class=" clearfix mr30"]/dd')
        for field in fields:
            if self.common_util.get_extract(field.xpath('strong/text()')) == '占地面积：':
                land_area = self.common_util.get_extract(field.xpath('text()'))
            if self.common_util.get_extract(field.xpath('strong/text()')) == '建筑面积：':
                building_area = self.common_util.get_extract(field.xpath('text()'))
            if self.common_util.get_extract(field.xpath('strong/text()')) == '物 业 费：':
                property_fee = self.common_util.get_extract(field.xpath('text()'))
        self.persistent_data.append(
            {
                'province_name': meta['province_name'],
                'city_name': meta['city_name'],
                'first_area': meta['first_area'],
                'second_area': meta['second_area'],
                'name': meta['name'],
                'url': meta['url'],
                'detail_url': meta['detail_url'],
                'price': meta['price'],
                'land_area': land_area,
                'building_area': building_area,
                'property_fee': property_fee
            }
        )
        self.save()

    def save(self):
        if len(self.persistent_data) > self.save_threshold:
            try:
                self.dao.customizable_add_ignore_batch(self.main_table, self.persistent_data, time=False)
            except AttributeError as e:
                self.dao = DaoUtils()
                self.dao.customizable_add_ignore_batch(self.main_table, self.persistent_data, time=False)
                print('save except:', e)
            finally:
                self.persistent_data = list()

    def save_final(self):
        if len(self.persistent_data) > 0:
            try:
                self.dao.customizable_add_ignore_batch(self.main_table, self.persistent_data, time=False)
            except AttributeError as e:
                self.dao = DaoUtils()
                self.dao.customizable_add_ignore_batch(self.main_table, self.persistent_data, time=False)
                print('save_final except:', e)
            finally:
                self.persistent_data = list()
