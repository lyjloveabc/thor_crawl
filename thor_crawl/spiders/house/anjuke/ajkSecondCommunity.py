"""
安居客-二手房-小区
"""
import scrapy
from scrapy import Selector
from scrapy.spiders import Spider

from thor_crawl.utils.commonUtil import CommonUtil
from thor_crawl.utils.db.daoUtil import DaoUtils
from thor_crawl.utils.db.mysql.mySQLConfig import MySQLConfig


class AjkSecondCommunity(Spider):
    name = 'house_ajk_second_community'
    handle_httpstatus_list = [301, 302, 204, 206, 404, 500]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ============ 工具 ============
        self.dao = DaoUtils(**{'dbType': 'MySQL', 'config': MySQLConfig.localhost()})
        self.common_util = CommonUtil()

        # ============ 持久化相关变量定义 ============
        self.save_threshold = 1000
        self.persistent_data = list()
        self.main_table = 'ajk_second_community'

    def __del__(self):
        self.save_final()

    def start_requests(self):
        start_requests = list()

        for row in self.dao.get_all('SELECT id, city_name, area_name, area_url FROM ajk_city_area WHERE city_name = "宁波" AND city_url_type = "SECOND";'):
            if row['area_url'] != '':
                start_requests.append(
                    scrapy.FormRequest(
                        url=row['area_url'], method='GET',
                        meta={'id': row['id'], 'city_name': row['city_name'], 'area_name': row['area_name']}
                    )
                )

        return start_requests

    def closed(self, res):
        self.save_final()

    def parse(self, response):
        body = response.body
        meta = response.meta
        hxf = Selector(text=body)
        url = response.url

        items = hxf.xpath('//div[@class="maincontent"]/div[@id="list-content"]/div[@class="li-itemmod"]')
        for item in items:
            db_obj = {
                'url': self.common_util.get_extract(item.xpath('div[1]/h3/a/@href')),
                'community_name': self.common_util.get_extract(item.xpath('div[1]/h3/a/text()')),

                'city_area_id': meta['id'],
                'city_name': meta['city_name'],
                'area_name': meta['area_name']
            }
            self.persistent_data.append(db_obj)

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
