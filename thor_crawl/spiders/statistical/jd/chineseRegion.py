"""
数据来自京东
https://d.jd.com/area/get?callback=getAreaListCallback&fid=4744
https://d.jd.com/area/get?fid=4744
"""
import json

import scrapy
from scrapy.spiders import BaseSpider

from thor_crawl.utils.commonUtil import CommonUtil
from thor_crawl.utils.db.daoUtil import DaoUtils


class ChineseRegion(BaseSpider):
    name = 'statistical_jd_chineseRegion'
    handle_httpstatus_list = [301, 302, 204, 206, 404, 500]

    start_urls = ['https://d.jd.com/area/get?fid=4744']

    def __init__(self):
        # ============ 工具 ============
        self.dao = DaoUtils()
        self.common_util = CommonUtil()

        # ============ 全局变量定义 ============
        self.main_table = 'chinese_region'
        self.base_url_format = 'https://d.jd.com/area/get?fid={fid}'

    def __del__(self):
        pass

    def closed(self, res):
        pass

    def parse(self, response):
        response_text = response.text
        meta = response.meta

        if '[ ]' != response_text:
            for region in json.loads(response_text):
                region_id = region['id']
                name = region['name']
                level = meta['level'] if 'level' in meta else 1

                db_region = {
                    'parent_id': meta['parent_id'] if 'parent_id' in meta else 0,
                    'name': name,
                    'level': level
                }
                parent_id = self.dao.customizable_add(self.main_table, db_region, time=True)

                if level < 4:
                    yield scrapy.FormRequest(url=self.base_url_format.format(fid=region_id), method='GET',
                                             meta={'parent_id': parent_id, 'level': level + 1})
