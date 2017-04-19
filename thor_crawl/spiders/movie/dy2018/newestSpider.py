"""
电影天堂 最新电影
http://www.dy2018.com/html/gndy/dyzz/index_2.html
"""
import re
import logging

import scrapy
from scrapy import Selector
from scrapy.spiders import Spider

from thor_crawl.utils.commonUtil import CommonUtil
from thor_crawl.utils.constant.constant import Constant
from thor_crawl.utils.db.daoUtil import DaoUtils


class NewestSpider(Spider):
    name = 'movie_dy2018_newest'
    handle_httpstatus_list = [204, 206, 301, 302, 404, 500]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logging.info(Constant.SPIDER_INIT)

        # ============ 工具 ============
        self.dao = DaoUtils()
        self.common_util = CommonUtil()

        self.domain = 'http://www.dy2018.com'
        self.base_url = 'http://www.dy2018.com/html/gndy/dyzz/index_{index}.html'

        # ============ 持久化 ============
        self.save_threshold = 100
        self.main_table = 'dy2018_newest'
        self.persistent_data = list()

    def __del__(self):
        logging.info(Constant.SPIDER_CLOSED)
        self.save_final()

    def start_requests(self):
        start_requests = list()

        meta = {'page_num': 1}
        form_request = scrapy.FormRequest(url='http://www.dy2018.com/html/gndy/dyzz/', method='GET', meta=meta)
        start_requests.append(form_request)

        return start_requests

    def closed(self, res):
        logging.info(Constant.SPIDER_CLOSED)
        self.save_final()

    def parse(self, response):
        text = response.text
        hxf = Selector(text=text)
        meta = response.meta

        movie_items = hxf.xpath('//div[@class="co_content8"]/ul/td/table')
        for item in movie_items:
            href = self.common_util.get_extract(item.xpath('tr[2]/td[2]/b/a/@href'))
            font_text = self.common_util.get_extract(item.xpath('tr[3]/td[2]/font/text()'))
            font_text_search = re.search(r'日期：(.+)\s+点击：(.+)', font_text)
            movie = {
                'dy2018_id': re.search(r'/i/(\d+).html', href).group(1),
                'name': self.common_util.get_extract(item.xpath('tr[2]/td[2]/b/a/text()')),
                'publish_day': font_text_search.group(1),
                'click_count': font_text_search.group(2),
                'detail_url': self.domain + self.common_util.get_extract(item.xpath('tr[3]/td[2]/font/text()'))
            }
            self.persistent_data.append(movie)

        # 下一页
        current_page_num = meta['page_num']
        total_num = re.search(r'第 (\d+) 页', self.common_util.get_extract(hxf.xpath('//select/option[last()]/text()'))).group(1)
        if current_page_num < int(total_num):
            next_page_num = current_page_num + 1
            meta = {'page_num': next_page_num}
            yield scrapy.FormRequest(url=self.base_url.format(index=next_page_num), method='GET', meta=meta)

    def save(self):
        if len(self.persistent_data) > self.save_threshold:
            try:
                self.dao.customizable_replace_batch(self.main_table, self.persistent_data)
            except AttributeError as e:
                self.dao = DaoUtils()
                self.dao.customizable_replace_batch(self.main_table, self.persistent_data)
                logging.error('save except:', e)
            finally:
                self.persistent_data = list()

    def save_final(self):
        if len(self.persistent_data) > 0:
            try:
                self.dao.customizable_replace_batch(self.main_table, self.persistent_data)
            except AttributeError as e:
                self.dao = DaoUtils()
                self.dao.customizable_replace_batch(self.main_table, self.persistent_data)
                logging.error('save_final except:', e)
            finally:
                self.persistent_data = list()
