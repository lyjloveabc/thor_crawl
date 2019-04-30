import re

import scrapy
from scrapy import Selector
from scrapy.spiders import Spider

from thor_crawl.spiders.spider_setting import DEFAULT_DB_ENV
from thor_crawl.utils.commonUtil import CommonUtil
from thor_crawl.utils.db.daoUtil import DaoUtils


class CityZoneNum(Spider):
    name = 'fang_zone'
    handle_httpstatus_list = [204, 206, 404, 500]

    start_urls = ['https://www.fang.com/SoufunFamily.htm']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ============ 工具 ============
        self.dao = DEFAULT_DB_ENV
        self.common_util = CommonUtil()

        # ============ 持久化相关变量定义 ============
        self.save_threshold = 20  # 一次性插入数据库阈值
        self.persistent_data = list()  # 内存暂存处理的数据，批量插入数据库
        self.main_table = 'fang_city_zone_num'  # 数据库存储表

        # ============ 业务数据 ============
        self.domain = 'https://{code}.esf.fang.com/housing/'
        self.base_url = 'https://{code}.esf.fang.com/housing/'
        self.bj_url = 'https://esf.fang.com/housing/'
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
        self.cities = dict()
        with open('city_after_format.txt', 'r') as f:
            for line in f.readlines():
                data = line.replace('\n', '')
                city_info = data.split(',')
                self.cities[city_info[1]] = {
                    'province_name': city_info[0],
                    'city_name': city_info[1],
                    'city_url': city_info[2],
                    'city_code': re.search(r'http://(.+)\.fang\.com', city_info[2]).group(1)
                }

    def __del__(self):
        self.save_final()

    def closed(self, res):
        self.save_final()

    def start_requests(self):
        start_requests = set()
        for row in self.need_city:
            if row in self.cities.keys():
                if row == '北京':
                    url = self.bj_url
                else:
                    url = self.base_url.format(code=self.cities[row]['city_code'])
                print(url)
                self.cities[row]['url'] = url
                start_requests.add(scrapy.FormRequest(url=url, method='GET', meta=self.cities[row]))
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

        num = self.common_util.get_extract(hxf.xpath('//div[@id="pxBox"]/p/b/text()'))
        self.persistent_data.append(
            {
                'province_name': meta['province_name'],
                'city_name': meta['city_name'],
                'num': num
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
