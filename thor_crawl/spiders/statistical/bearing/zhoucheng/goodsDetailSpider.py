"""
中国轴承产业服务平台 商品详情
"""

import scrapy
from scrapy import Selector
from scrapy.spiders import Spider

from thor_crawl.utils.commonUtil import CommonUtil
from thor_crawl.utils.db.daoUtil import DaoUtils


class GoodsDetailSpider(Spider):
    name = 'bearing_zc_goodsDetail'
    handle_httpstatus_list = [301, 302, 204, 206, 404, 500]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ============ 工具 ============
        self.dao = DaoUtils()
        self.common_util = CommonUtil()

        # ============ 持久化相关变量定义 ============
        self.save_threshold = 1000
        self.persistent_data = list()
        self.main_table = 'bearing_zc_goods'
        self.domain = 'http://www.zhoucheng.cn'

    def start_requests(self):
        goods_items = self.dao.customizable_get_all('bearing_zc_goods', ['id', 'detail_url'])

        start_requests = set()
        for goods in goods_items:
            meta = {
                'id': goods['id']
            }
            form_request = scrapy.FormRequest(url=self.domain + goods['detail_url'], method='GET', meta=meta)
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

        goods_detail_content = hxf.xpath('//div[@class="goods"]')
        if len(goods_detail_content) <= 0:
            goods_detail_content = hxf.xpath('//div[@class="good-content"]')

        images = self.domain + self.common_util.get_extract(goods_detail_content.xpath('div[1]/div[1]/div[1]/a[1]/img/@src'))

        minimum_order_quantity = self.common_util.get_extract(goods_detail_content.xpath('div[1]/div[2]/p[1]/span/text()'))
        warranty_time = self.common_util.get_extract(goods_detail_content.xpath('div[1]/div[2]/p[2]/text()'))
        brand = self.common_util.get_extract(goods_detail_content.xpath('div[1]/div[2]/p[3]/text()'))
        price = self.common_util.get_extract(goods_detail_content.xpath('div[1]/div[2]/p[5]/span/text()'))
        volume = self.common_util.get_extract(goods_detail_content.xpath('div[1]/div[2]/p[7]/text()'))
        release_time = self.common_util.get_extract(goods_detail_content.xpath('div[1]/div[2]/p[8]/text()'))

        new_model = self.common_util.get_extract(goods_detail_content.xpath('div[2]/table/tbody/tr[1]/td[2]/text()'))
        old_model = self.common_util.get_extract(goods_detail_content.xpath('div[2]/table/tbody/tr[1]/td[4]/text()'))
        bearing_material = self.common_util.get_extract(goods_detail_content.xpath('div[2]/table/tbody/tr[2]/td[4]/text()'))
        inner_diameter = self.common_util.get_extract(goods_detail_content.xpath('div[2]/table/tbody/tr[3]/td[2]/text()'))
        outer_diameter = self.common_util.get_extract(goods_detail_content.xpath('div[2]/table/tbody/tr[3]/td[4]/text()'))
        weight = self.common_util.get_extract(goods_detail_content.xpath('div[2]/table/tbody/tr[4]/td[2]/text()'))
        width = self.common_util.get_extract(goods_detail_content.xpath('div[2]/table/tbody/tr[4]/td[4]/text()'))
        cage_materials = self.common_util.get_extract(goods_detail_content.xpath('div[2]/table/tbody/tr[5]/td[2]/text()'))
        use_text = self.common_util.get_extract(goods_detail_content.xpath('div[2]/table/tbody/tr[6]/span/text()'))

        goods = {
            'images': images,
            'minimum_order_quantity': minimum_order_quantity,
            'warranty_time': warranty_time,
            'brand': brand,
            'price': price,
            'volume': volume,
            'release_time': release_time,
            'new_model': new_model,
            'old_model': old_model,
            'bearing_material': bearing_material,
            'inner_diameter': inner_diameter,
            'outer_diameter': outer_diameter,
            'weight': weight,
            'width': width,
            'cage_materials': cage_materials,
            'use_text': use_text
        }
        self.persistent_data.append(goods)
        self.dao.customizable_modify(self.main_table, goods, {'id': meta['id']})

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

    def modify(self):
        if len(self.persistent_data) > self.save_threshold:
            try:
                self.dao.customizable_add_batch(self.main_table, self.persistent_data)
            except AttributeError as e:
                self.dao = DaoUtils()
                self.dao.customizable_add_batch(self.main_table, self.persistent_data)
                print('save except:', e)
            finally:
                self.persistent_data = list()
