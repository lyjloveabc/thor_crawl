"""
算算你再杭州的租房成本
"""

from scrapy import Selector
from scrapy.spiders import Spider

from thor_crawl.utils.commonUtil import CommonUtil
from thor_crawl.utils.db.daoUtil import DaoUtils
from thor_crawl.utils.db.mysql.mySQLConfig import MySQLConfig


class RentInHz(Spider):
    name = 'house_fang_city'
    handle_httpstatus_list = [301, 302, 204, 206, 404, 500]

    start_urls = ['http://hz.zu.fang.com/']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ============ 工具 ============
        self.dao = DaoUtils(**{'dbType': 'MySQL', 'config': MySQLConfig.localhost()})
        self.common_util = CommonUtil()

        # ============ 持久化相关变量定义 ============
        self.save_threshold = 1000
        self.persistent_data = list()
        self.main_table = 'fang'

    def __del__(self):
        self.save_final()

    def closed(self, res):
        self.save_final()

    def parse(self, response):
        body = response.body
        meta = response.meta
        hxf = Selector(text=body)

        lis = hxf.xpath('//div[@class="content"]/div[@class="city-itm"]/div[2]/ul/li')
        for li in lis[:-1]:
            a_s = li.xpath('div[1]/a')
            for a in a_s:
                self.persistent_data.append(
                    {
                        'name': self.common_util.get_extract(a.xpath('text()')),
                        'url': self.common_util.get_extract(a.xpath('@href'))
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
