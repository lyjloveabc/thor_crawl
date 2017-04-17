"""
中国轴承产业服务平台 商品
"""
import re

import scrapy
from scrapy import Selector
from scrapy.spiders import Spider

from thor_crawl.utils.commonUtil import CommonUtil
from thor_crawl.utils.db.daoUtil import DaoUtils


class GoodsSpider(Spider):
    name = 'bearing_zc_goods'
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

    def start_requests(self):
        goods_category_items = self.dao.customizable_get_all('bearing_zc_goods_category', ['id', 'url', 'name'])

        start_requests = set()
        for goods_category in goods_category_items:
            __EVENTARGUMENT = '1'
            form_data = {
                # '__VIEWSTATE': '',
                '__EVENTTARGET': 'AspNetPager1',
                '__EVENTARGUMENT': __EVENTARGUMENT,
                # 'UCTop$txtMove': goods_category['name'],
                # 'UCTop$txtMoveInside': '',
                # 'UCTop$txtMoveOutside': '',
                # 'UCTop$txtMoveWidth': '',
                # 'UCTop$txtHead': goods_category['name'],
                # 'UCTop$txtHeadInside': '',
                # 'UCTop$txtHeadOutside': '',
                # 'UCTop$txtHeadWidth': '',
                # 'hidDisplayType': '-1',
            }
            meta = {
                'category_id': goods_category['id'],
                'category_name': goods_category['name']
            }
            form_request = scrapy.FormRequest(url=goods_category['url'], method='POST', formdata=form_data, meta=meta)
            start_requests.add(form_request)

        return start_requests

    def __del__(self):
        self.save_final()

    def closed(self, res):
        self.save_final()

    def parse(self, response):
        body = response.body
        meta = response.meta
        hxf = Selector(text=body)
        url = response.url

        search_list = hxf.xpath('//ul[@class="search-list"]/li')
        if len(search_list) > 0:
            for goods_item in search_list:
                goods = {
                    'name': self.common_util.get_extract(goods_item.xpath('div[1]/a/@title')),
                    'category_id': meta['category_id'],
                    'category_name': meta['category_name'],
                    'model': self.common_util.get_extract(goods_item.xpath('div[2]/p[2]/text()')),
                    'detail_url': self.common_util.get_extract(goods_item.xpath('div[1]/a/@href'))
                }
                self.persistent_data.append(goods)

        self.save()

        # 下一页
        page_num_text = self.common_util.get_extract(hxf.xpath('//div[@id="AspNetPager4"]/div[2]/text()'))
        print(page_num_text)
        if page_num_text != '':
            page_nums = re.search(r'第 (\d+)/(\d+) 页', page_num_text).groups()
            current_page_num = int(page_nums[0])
            total_page_num = int(page_nums[1])
            if len(page_nums) >= 2 and current_page_num < total_page_num:
                next_page_num = current_page_num + 1
                form_data = {
                    '__EVENTTARGET': 'AspNetPager1',
                    '__EVENTARGUMENT': str(next_page_num)
                }
                yield scrapy.FormRequest(url=url, method='POST', formdata=form_data, meta=meta)
        else:
            pass

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
