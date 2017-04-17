"""
搜轴网 商品
"""
import json
import re

import scrapy
from scrapy.spiders import Spider

from thor_crawl.utils.commonUtil import CommonUtil
from thor_crawl.utils.db.daoUtil import DaoUtils


class GoodsSpider(Spider):
    name = 'bearing_soz_goods'
    handle_httpstatus_list = [301, 302, 204, 206, 404, 500]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ============ 工具 ============
        self.dao = DaoUtils()
        self.common_util = CommonUtil()

        # ============ 持久化相关变量定义 ============
        self.save_threshold = 1000
        self.persistent_data = list()
        self.main_table = 'bearing_soz_goods'
        self.domain = 'http://www.sozhou.com'
        self.start_url = 'http://www.sozhou.com/tools/submit_ajax.ashx?action=model_list_aa&pp={pp}&click={click}'

    def start_requests(self):
        click = 1
        brand_items = self.dao.customizable_get_all('bearing_soz_brand', ['id', 'brand', 'url', 'type'])
        print(len(brand_items))

        start_requests = set()
        for brand in brand_items:
            pp = re.search(r'/prdt/(\d*)\.html', brand['url']).group(1)
            url = self.start_url.format(pp=pp, click=click)
            meta = {
                'brand_id': brand['id'],
                'pp': pp,
                'click': click,
                'type': brand['type']
            }
            form_request = scrapy.FormRequest(url=url, method='POST', meta=meta)
            start_requests.add(form_request)

        return start_requests

    def __del__(self):
        self.save_final()

    def closed(self, res):
        self.save_final()

    def parse(self, response):
        body = response.body
        meta = response.meta

        body_text = body.decode('utf-8')
        if body_text != '要查看更多，请联系商家':
            for goods_info in json.loads(body_text):
                if 'model' in goods_info:
                    model = goods_info['model']
                    img = goods_info['img']
                    strurl = goods_info['strurl']
                    idcode = goods_info['idcode']
                    brand = goods_info['brand']
                    model_len = goods_info['model_len']

                    goods = {
                        'brand_id': meta['brand_id'],
                        'model': model,
                        'brand': brand,
                        # 'series': series,
                        # 'inner_diameter': inner_diameter,
                        # 'outer_diameter': outer_diameter,
                        # 'weight': weight,
                        'images': self.domain + img,
                        'type': '进口' if meta['type'] == 'import' else '国产',
                        'detail_url': self.domain + '/' + strurl + '/' + idcode + '.html'
                    }
                    self.persistent_data.append(goods)

            # 下一页
            meta['click'] += 1
            next_url = self.start_url.format(pp=meta['pp'], click=meta['click'])
            yield scrapy.FormRequest(url=next_url, method='POST', meta=meta)

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
