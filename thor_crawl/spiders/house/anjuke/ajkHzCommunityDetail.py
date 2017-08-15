"""
安居客-杭州-所有的二手房小区
"""
import scrapy
from scrapy import Selector
from scrapy.spiders import Spider

from thor_crawl.utils.commonUtil import CommonUtil
from thor_crawl.utils.db.daoUtil import DaoUtils


class AjkHzCommunityDetail(Spider):
    name = 'ajk_hz_community_detail'
    handle_httpstatus_list = [204, 206, 404, 500]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ============ 工具 ============
        self.dao = DaoUtils()
        self.common_util = CommonUtil()

        # ============ 持久化相关变量定义 ============
        self.save_threshold = 0
        self.persistent_data = list()
        self.main_table = 'ajk_hz_community_detail'
        self.base_url = 'https://hangzhou.anjuke.com'

    def start_requests(self):
        items = self.dao.get_all('SELECT id, hz_area_id, hz_area_name, url, name, community_address, village_house_price FROM ajk_hz_community ORDER BY id')

        start_requests = set()
        for item in items:
            meta = {
                'id': item['id'],
                'hz_area_id': item['hz_area_id'],
                'hz_area_name': item['hz_area_name'],
                'name': item['name'],
                'community_address': item['community_address'],
                'village_house_price': item['village_house_price']
            }
            form_request = scrapy.FormRequest(url=self.base_url + item['url'], method='GET', meta=meta)
            start_requests.add(form_request)

        return start_requests

    def __del__(self):
        self.save_final()

    def closed(self, res):
        self.save_final()

    def parse(self, response):
        text = response.text
        meta = response.meta
        hxf = Selector(text=text)

        item = hxf.xpath('//div[@id="basic-infos-box"]/dl[@class="basic-parms-mod"]')
        db_obj = {
            'hz_area_id': meta['hz_area_id'],
            'hz_area_name': meta['hz_area_name'],
            'community_name': meta['name'],
            'community_address': meta['community_address'],

            'property_type': self.common_util.get_extract(item.xpath('dd[1]/text()')),
            'property_fee': self.common_util.get_extract(item.xpath('dd[2]/text()')),
            'total_area': self.common_util.get_extract(item.xpath('dd[3]/text()')),
            'total_house': self.common_util.get_extract(item.xpath('dd[4]/text()')),
            'build_year': self.common_util.get_extract(item.xpath('dd[5]/text()')),
            'parking': self.common_util.get_extract(item.xpath('dd[6]/text()')),
            'plot_ratio': self.common_util.get_extract(item.xpath('dd[7]/text()')),
            'developer': self.common_util.get_extract(item.xpath('dd[9]/text()')),
            'property_company': self.common_util.get_extract(item.xpath('dd[10]/text()')),

            'village_house_price': meta['village_house_price']
        }
        self.persistent_data.append(db_obj)

        print(1)
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
