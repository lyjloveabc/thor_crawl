# coding=utf-8
import re

import scrapy
from scrapy import Selector
from scrapy.spiders import Spider

from thor_crawl.spiders.spider_setting import DEFAULT_DB_ENV
from thor_crawl.utils.commonUtil import CommonUtil
from thor_crawl.utils.db.daoUtil import DaoUtils
from thor_crawl.utils.email.emailUtil import EmailUtils

import sys
from imp import reload
reload(sys)
sys.setdefaultencoding('utf8')


class CityZone(Spider):
    name = 'fang_city_zone'
    handle_httpstatus_list = [204, 206, 404, 500]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ============ 工具 ============
        self.dao = DEFAULT_DB_ENV
        self.common_util = CommonUtil()

        # ============ 持久化相关变量定义 ============
        self.save_threshold = 20  # 一次性插入数据库阈值
        self.persistent_data = list()  # 内存暂存处理的数据，批量插入数据库
        self.main_table = 'fang_city_zone'  # 数据库存储表

        # ============ 业务数据 ============
        self.need_city = ['上海',
                          '北京',
                          '深圳',
                          '广州',
                          '成都',
                          '杭州',
                          '重庆',
                          '武汉',
                          '苏州',
                          '西安',
                          '天津',
                          '南京',
                          '郑州',
                          '长沙',
                          '沈阳',
                          '青岛',
                          '宁波',
                          '东莞',
                          '无锡',
                          '昆明',
                          '大连',
                          '厦门',
                          '合肥',
                          '佛山',
                          '福州',
                          '哈尔滨',
                          '济南',
                          '温州',
                          '长春',
                          '石家庄',
                          '常州',
                          '泉州',
                          '南宁',
                          '贵阳',
                          '南昌',
                          '南通',
                          '金华',
                          '徐州',
                          '太原',
                          '嘉兴',
                          '烟台',
                          '惠州',
                          '保定',
                          '台州',
                          '中山',
                          '绍兴',
                          '乌鲁木齐',
                          '潍坊',
                          '兰州']
        self.sign = '/housing/'
        self.detail_sign = 'xiangqing'

        other_url = 'https://{code}.esf.fang.com'
        bj_url = 'https://esf.fang.com/housing'
        self.cities = dict()
        with open('city_after_format.txt', 'r') as f:
            for line in f.readlines():
                data = line.replace('\n', '')
                city_info = data.split(',')
                code = re.search(r'http://(.+)\.fang\.com', city_info[2]).group(1)
                self.cities[city_info[1]] = {
                    'province_name': city_info[0],
                    'city_name': city_info[1],
                    'city_index_url': city_info[2],
                    'city_base_url': bj_url if city_info[1] == '北京' else other_url.format(code=code),
                    'city_code': code
                }

    def __del__(self):
        self.save_final()

    def closed(self, res):
        EmailUtils.send_mail('挂了！！！', '挂了')
        self.save_final()

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
            yield scrapy.FormRequest(url='https:' + meta['url'], method='GET', meta=meta, callback=self.parse_zone_index)

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
        fields = hxf.xpath('//dl[@class=" clearfix mr30"]/dd')
        for field in fields:
            if self.common_util.get_extract(field.xpath('strong/text()')) == '占地面积：':
                land_area = self.common_util.get_extract(field.xpath('text()'))
            if self.common_util.get_extract(field.xpath('strong/text()')) == '建筑面积：':
                building_area = self.common_util.get_extract(field.xpath('text()'))
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
                'building_area': building_area
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
