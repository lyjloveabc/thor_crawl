"""
搜轴网 商品详情
"""
import scrapy
from scrapy import Selector
from scrapy.spiders import BaseSpider

from thor_crawl.utils.commonUtil import CommonUtil
from thor_crawl.utils.db.daoUtil import DaoUtils


class GoodsDetailSpider(BaseSpider):
    name = 'bearing_soz_goodsDetail'
    handle_httpstatus_list = [301, 302, 204, 206, 404, 500]

    def __init__(self):
        # ============ 工具 ============
        self.dao = DaoUtils()
        self.common_util = CommonUtil()

        # ============ 持久化相关变量定义 ============
        self.save_threshold = 1000
        self.persistent_data = list()
        self.main_table = 'bearing_soz_goods'
        self.domain = 'http://www.sozhou.com/'

    def start_requests(self):
        # goods_items = self.dao.customizable_get_all(self.main_table, ['id', 'detail_url'])
        goods_items = self.dao.get_all('select id, detail_url from bearing_soz_goods where inner_diameter = \'\' order by id')

        start_requests = set()
        for goods in goods_items:
            meta = {
                'id': goods['id']
            }
            form_request = scrapy.FormRequest(url=goods['detail_url'], method='GET', meta=meta)
            start_requests.add(form_request)

        return start_requests

    def __del__(self):
        pass

    def closed(self, res):
        pass

    def parse(self, response):
        body = response.body
        hxf = Selector(text=body)
        meta = response.meta
        print(response.request.headers)

        goods_info = hxf.xpath('//div[@class="view"]/div[@class="rt"]/div[@class="left-mod"]')

        series = self.common_util.get_extract(goods_info.xpath('div[@class="dd"]/dt[3]/text()'))
        inner_diameter = self.common_util.get_extract(goods_info.xpath('div[@class="dd"]/dt[4]/text()'))
        outer_diameter = self.common_util.get_extract(goods_info.xpath('div[@class="dd"]/dt[5]/text()'))
        width = self.common_util.get_extract(goods_info.xpath('div[@class="dd"]/dt[6]/text()'))

        images = self.common_util.get_extract(hxf.xpath('//div[@class="view"]/div[@class="lt"]/div/div/div[@class="picBox"]/ul/li[1]/a/img/@src'))

        goods = {
            'series': series,
            'inner_diameter': inner_diameter,
            'outer_diameter': outer_diameter,
            'width': width,
            'images': images
        }
        self.dao.customizable_modify(self.main_table, goods, {'id': meta['id']})
