"""
安居客-某个城市-所有的区域
"""
import scrapy
from scrapy import Selector
from scrapy.spiders import Spider

from thor_crawl.utils.commonUtil import CommonUtil
from thor_crawl.utils.db.daoUtil import DaoUtils
from thor_crawl.utils.db.mysql.mySQLConfig import MySQLConfig


class AjkCityArea(Spider):
    name = 'house_ajk_city_area'
    handle_httpstatus_list = [301, 302, 204, 206, 404, 500]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ============ 工具 ============
        self.dao = DaoUtils(**{'dbType': 'MySQL', 'config': MySQLConfig.localhost()})
        self.common_util = CommonUtil()

        # ============ 持久化相关变量定义 ============
        self.save_threshold = 1000
        self.persistent_data = list()
        self.main_table = 'ajk_city_area'

    def __del__(self):
        self.save_final()

    def start_requests(self):
        start_requests = list()

        for row in self.dao.get_all('SELECT id, city_name, type, url FROM ajk_city_inlet WHERE city_name IN ("南京") AND type = "SECOND"'):
            if row['url'] != '':
                start_requests.append(scrapy.FormRequest(url=row['url'], method='GET', meta={'id': row['id'], 'city_name': row['city_name'], 'type': row['type']}))

        return start_requests

    def closed(self, res):
        self.save_final()

    def parse(self, response):
        body = response.body
        meta = response.meta
        hxf = Selector(text=body)
        url = response.url

        if meta['type'] == 'NEW':
            total = self.common_util.get_extract(
                hxf.xpath('//div[@id="container"]/div[@class="list-contents"]/div[@class="list-results"]/div[@class="key-sort"]/div[@class="sort-condi"]/span/em/text()')
            )

            if total != '':
                self.dao.dao.execute('UPDATE ajk_city_inlet SET total = "{total}" WHERE url = "{url}"'.format(total=total, url=url))

            a_s = hxf.xpath('//div[@class="filter"]/a')

            for a in a_s:
                self.persistent_data.append(
                    {
                        'city_inlet_id': meta['id'],
                        'city_inlet_type': meta['type'],
                        'city_name': meta['city_name'],
                        'area_name': self.common_util.get_extract(a.xpath('text()')),
                        'area_url': self.common_util.get_extract(a.xpath('@href'))
                    }
                )
        elif meta['type'] == 'SECOND':
            a_s = hxf.xpath('//div[@class="w1180"]/div[2]/div[1]/span[2]/a')

            for a in a_s[1:]:
                self.persistent_data.append(
                    {
                        'city_inlet_id': meta['id'],
                        'city_inlet_type': meta['type'],
                        'city_name': meta['city_name'],
                        'area_name': self.common_util.get_extract(a.xpath('text()')),
                        'area_url': self.common_util.get_extract(a.xpath('@href'))
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
