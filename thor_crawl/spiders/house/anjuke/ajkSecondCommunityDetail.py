"""
安居客-二手房-小区
"""
import scrapy
from scrapy import Selector
from scrapy.spiders import Spider

from thor_crawl.utils.commonUtil import CommonUtil
from thor_crawl.utils.db.daoUtil import DaoUtils
from thor_crawl.utils.db.mysql.mySQLConfig import MySQLConfig


class AjkSecondCommunityDetail(Spider):
    name = 'house_ajk_second_community_detail'
    handle_httpstatus_list = [301, 302, 204, 206, 404, 500]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ============ 工具 ============
        self.dao = DaoUtils(**{'dbType': 'MySQL', 'config': MySQLConfig.localhost()})
        self.common_util = CommonUtil()

        # ============ 持久化相关变量定义 ============
        self.save_threshold = 10
        self.persistent_data = list()
        self.main_table = 'ajk_second_community_detail'
        self.base_url = 'https://hangzhou.anjuke.com'

    def __del__(self):
        self.save_final()

    def start_requests(self):
        start_requests = list()

        for row in self.dao.get_all('SELECT id, area_name, community_name, url FROM ajk_second_community;'):
            if row['url'] != '':
                start_requests.append(
                    scrapy.FormRequest(
                        url=self.base_url + row['url'], method='GET',
                        meta={'id': row['id'], 'area_name': row['area_name'], 'community_name': row['community_name']}
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

        item = hxf.xpath('//div[@id="basic-infos-box"]/dl[@class="basic-parms-mod"]')
        db_obj = {
            'city_area_id': meta['id'],
            'area_name': meta['area_name'],
            'community_name': meta['community_name'],

            'community_address': self.common_util.get_extract(hxf.xpath('//div[@id="content"]/div[3]/div[1]/h1/span/text()')),
            'property_type': self.common_util.get_extract(item.xpath('dd[1]/text()')),
            'property_fee': self.common_util.get_extract(item.xpath('dd[2]/text()')),
            'total_area': self.common_util.get_extract(item.xpath('dd[3]/text()')),
            'total_house': self.common_util.get_extract(item.xpath('dd[4]/text()')),
            'build_year': self.common_util.get_extract(item.xpath('dd[5]/text()')),
            'parking': self.common_util.get_extract(item.xpath('dd[6]/text()')),
            'plot_ratio': self.common_util.get_extract(item.xpath('dd[7]/text()')),
            'developer': self.common_util.get_extract(item.xpath('dd[9]/text()')),
            'property_company': self.common_util.get_extract(item.xpath('dd[10]/text()')),

            'village_house_price': self.common_util.get_extract(hxf.xpath('//div[@id="basic-infos-box"]/div[@class="price"]/span[1]/text()')) +
                                   self.common_util.get_extract(hxf.xpath('//div[@id="basic-infos-box"]/div[@class="price"]/span[1]/em/text()')),
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
