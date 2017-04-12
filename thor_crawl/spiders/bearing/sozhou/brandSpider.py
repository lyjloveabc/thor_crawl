"""
搜轴网 商品品牌
"""
from scrapy import Selector
from scrapy.spiders import BaseSpider

from thor_crawl.utils.commonUtil import CommonUtil
from thor_crawl.utils.db.daoUtil import DaoUtils


class BrandSpider(BaseSpider):
    name = 'bearing_soz_brand'
    handle_httpstatus_list = [301, 302, 204, 206, 404, 500]

    start_urls = ['http://www.sozhou.com/prdt_2.html']

    def __init__(self):
        # ============ 工具 ============
        self.dao = DaoUtils()
        self.common_util = CommonUtil()

        # ============ 持久化相关变量定义 ============
        self.save_threshold = 1000
        self.persistent_data = list()
        self.main_table = 'bearing_soz_brand'

    def __del__(self):
        self.save_final()

    def closed(self, res):
        self.save_final()

    def parse(self, response):
        body = response.body
        hxf = Selector(text=body)

        brand_items = hxf.xpath('//div[@class="main"]/div[@class="content"]/div/div[1]/div[2]/ul/li')
        for brand_dom in brand_items:
            brand_dom_class = self.common_util.get_extract(brand_dom.xpath('@class'))
            brand_url = self.common_util.get_extract(brand_dom.xpath('a/@href'))
            brand_name = self.common_util.get_extract(brand_dom.xpath('a/text()'))

            brand = {
                'brand': brand_name,
                'url': brand_url,
                'type': brand_dom_class,
            }

            self.persistent_data.append(brand)
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
