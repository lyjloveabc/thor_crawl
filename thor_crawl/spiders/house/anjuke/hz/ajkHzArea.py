"""
安居客-杭州-所有的区域
"""

from scrapy import Selector
from scrapy.spiders import Spider

from thor_crawl.utils.commonUtil import CommonUtil
from thor_crawl.utils.db.daoUtil import DaoUtils


class AjkHzArea(Spider):
    name = 'house_ajk_hz_area'
    handle_httpstatus_list = [301, 302, 204, 206, 404, 500]

    start_urls = ['https://hangzhou.anjuke.com/community/']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ============ 工具 ============
        self.dao = DaoUtils()
        self.common_util = CommonUtil()

        # ============ 持久化相关变量定义 ============
        self.save_threshold = 1000
        self.persistent_data = list()
        self.main_table = 'ajk_hz_area'

    def __del__(self):
        self.save_final()

    def closed(self, res):
        self.save_final()

    def parse(self, response):
        body = response.body
        meta = response.meta
        hxf = Selector(text=body)

        items = hxf.xpath('//div[@class="w1180"]/div[@class="div-border items-list"]/div[@class="items"]/span[2]/a')
        for item in items:
            ajk_area = {
                'base_url': self.common_util.get_extract(item.xpath('@href')),
                'name': self.common_util.get_extract(item.xpath('text()'))
            }
            self.persistent_data.append(ajk_area)

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
