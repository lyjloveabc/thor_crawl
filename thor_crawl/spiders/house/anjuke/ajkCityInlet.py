"""
安居客-城市的新房、二手房的入口
"""
import scrapy
from scrapy import Selector
from scrapy.spiders import Spider

from thor_crawl.utils.commonUtil import CommonUtil
from thor_crawl.utils.db.daoUtil import DaoUtils
from thor_crawl.utils.db.mysql.mySQLConfig import MySQLConfig


class AjkCityInlet(Spider):
    name = 'house_ajk_city_inlet'
    handle_httpstatus_list = [301, 302, 204, 206, 404, 500]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ============ 工具 ============
        self.dao = DaoUtils(**{'dbType': 'MySQL', 'config': MySQLConfig.localhost()})
        self.common_util = CommonUtil()

        # ============ 持久化相关变量定义 ============
        self.save_threshold = 1000
        self.persistent_data = list()
        self.main_table = 'ajk_city_inlet'

    def __del__(self):
        self.save_final()

    def start_requests(self):
        start_requests = list()

        for row in self.dao.get_all('SELECT id, name, url FROM ajk_city'):
            start_requests.append(scrapy.FormRequest(url=row['url'], method='GET', meta={'id': row['id'], 'name': row['name']}))

        return start_requests

    def closed(self, res):
        self.save_final()

    def parse(self, response):
        body = response.body
        meta = response.meta
        hxf = Selector(text=body)

        new = hxf.xpath('//div[@id="glbNavigation"]/div[1]/ul/li[2]/a/@href')
        second = hxf.xpath('//div[@id="glbNavigation"]/div[1]/ul/li[3]/div[1]/a[2]/@href')
        self.persistent_data.append(
            {
                'city_id': meta['id'],
                'city_name': meta['name'],
                'type': 'NEW',
                'url': self.common_util.get_extract(new),
            }
        )
        self.persistent_data.append(
            {
                'city_id': meta['id'],
                'city_name': meta['name'],
                'type': 'SECOND',
                'url': self.common_util.get_extract(second),
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
