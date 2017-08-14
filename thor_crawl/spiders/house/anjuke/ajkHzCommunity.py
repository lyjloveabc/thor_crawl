"""
安居客-杭州-所有的二手房小区
"""
import scrapy
from scrapy import Selector
from scrapy.spiders import Spider

from thor_crawl.utils.commonUtil import CommonUtil
from thor_crawl.utils.db.daoUtil import DaoUtils


class AjkHzCommunity(Spider):
    name = 'house_ajk_hz_community'
    # handle_httpstatus_list = [301, 302, 204, 206, 404, 500]
    handle_httpstatus_list = [204, 206, 404, 500]

    start_urls = ['https://hangzhou.anjuke.com/community/']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ============ 工具 ============
        self.dao = DaoUtils()
        self.common_util = CommonUtil()

        # ============ 持久化相关变量定义 ============
        self.save_threshold = 100
        self.persistent_data = list()
        self.main_table = 'ajk_hz_community'

    def start_requests(self):
        items = self.dao.get_all('SELECT base_url, name, id FROM ajk_hz_area WHERE id > 1')

        start_requests = set()
        for item in items:
            base_url = str(item['base_url']) + 'p1'
            meta = {
                'name': item['name'],
                'url': str(item['base_url']) + 'p{pn}',
                'id': item['id']
            }
            form_request = scrapy.FormRequest(url=base_url, method='GET', meta=meta)
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

        items = hxf.xpath('//div[@class="maincontent"]/div[@id="list-content"]/div[@class="li-itemmod"]')
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
