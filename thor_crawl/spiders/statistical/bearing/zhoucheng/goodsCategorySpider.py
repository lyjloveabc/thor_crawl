"""
中国轴承产业服务平台 商品类别
"""
from scrapy import Selector
from scrapy.spiders import Spider

from thor_crawl.utils.commonUtil import CommonUtil
from thor_crawl.utils.db.daoUtil import DaoUtils


class GoodsCategorySpider(Spider):
    name = 'bearing_zc_goodsCategory'
    handle_httpstatus_list = [301, 302, 204, 206, 404, 500]

    start_urls = ['http://www.zhoucheng.cn/']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ============ 工具 ============
        self.dao = DaoUtils()
        self.common_util = CommonUtil()

        # ============ 持久化相关变量定义 ============
        self.save_threshold = 1000
        self.persistent_data = list()
        self.main_table = 'bearing_zc_goods_category'

    def __del__(self):
        self.save_final()

    def closed(self, res):
        self.save_final()

    def parse(self, response):
        body = response.body
        hxf = Selector(text=body)

        category_items = hxf.xpath('//ul[@id="content_2"]/li')
        for category_dom in category_items:
            category_name = self.common_util.get_extract(category_dom.xpath('a/text()'))
            category = {
                'name': category_name,
                'url': 'http://www.zhoucheng.cn/User/HeadSearch/SearchBearing.aspx?SearchType=类型&SearchText=' + category_name
            }
            self.persistent_data.append(category)

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
