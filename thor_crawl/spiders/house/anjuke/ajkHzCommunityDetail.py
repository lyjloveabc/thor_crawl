"""
安居客-杭州-所有的二手房小区
"""
import scrapy
from scrapy import Selector
from scrapy.spiders import Spider

from thor_crawl.utils.commonUtil import CommonUtil
from thor_crawl.utils.db.daoUtil import DaoUtils


class AjkHzCommunityDetail(Spider):
    name = 'house_ajk_hz_community_detail'
    handle_httpstatus_list = [204, 206, 404, 500]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ============ 工具 ============
        self.dao = DaoUtils()
        self.common_util = CommonUtil()

        # ============ 持久化相关变量定义 ============
        self.save_threshold = 100
        self.persistent_data = list()
        self.main_table = 'ajk_hz_community'
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

        items = hxf.xpath('//div[@id="container"]/div[@id="content"]/div[@class="comm-basic-mod"]/div[@id="basic-infos-box"]/div[@class="basic-parms-mod"]')
        for item in items:
            db_obj = {
                'url': self.common_util.get_extract(item.xpath('div[1]/h3/a/@href')),
                'name': self.common_util.get_extract(item.xpath('div[1]/h3/a/text()')),
                'community_address': self.common_util.get_extract(item.xpath('div[1]/address/text()')),
                'date': self.common_util.get_extract(item.xpath('div[1]/p[@class="date"]/text()')),
                'village_house_price': self.common_util.get_extract(item.xpath('div[2]/p[1]/strong/text()')),

                'hz_area_id': meta['id'],
                'hz_area_name': meta['name']
            }
            self.persistent_data.append(db_obj)

        self.save()

        # 下一页
        if len(items) > 0:
            try:
                next_page_info = hxf.xpath('//div[@class="maincontent"]/div[@class="page-content"]')
                this_page_num = int(self.common_util.get_extract(next_page_info.xpath('div/i[@class="curr"]/text()')))

                next_page_url = meta['url'].format(pn=this_page_num + 1)
                yield scrapy.FormRequest(url=next_page_url, method='GET', meta=meta)
            except Exception:
                print(meta)

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
