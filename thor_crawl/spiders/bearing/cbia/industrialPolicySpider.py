"""
中国轴承行业网 产业政策
"""
import re
from datetime import datetime

import scrapy
from scrapy import Selector
from scrapy.spiders import BaseSpider

from thor_crawl.utils.commonUtil import CommonUtil
from thor_crawl.utils.db.daoUtil import DaoUtils


class IndustrialPolicySpider(BaseSpider):
    name = 'bearing_cbia_industrial_policy'
    handle_httpstatus_list = [301, 302, 204, 206, 404, 500]

    start_urls = [
        'http://www.cbia.com.cn/index.php/Home/Infoforum/foruminfolist/code/AT1451446685AKPQ?&page=1'
    ]

    def __init__(self):
        # ============ 工具 ============
        self.dao = DaoUtils()
        self.common_util = CommonUtil()

        # ============ 持久化相关变量定义 ============
        self.save_threshold = 1000
        self.persistent_data = list()
        self.now_day = datetime.today().strftime('%Y%m%d')
        self.now_item_num = 0
        self.base_url = 'http://www.cbia.com.cn/index.php/Home/Infoforum/foruminfolist/code/AT1451446685AKPQ?&page={page}'
        self.base_detail_url = 'http://www.cbia.com.cn/index.php/Home/Infoforum/infodetail/code/{code}'
        self.file_name = '中国轴承行业网_' + '产业政策' + '_' + self.now_day + '.txt'
        self.file_path = 'spiders/bearing/cbia/file/'

    def __del__(self):
        pass

    def closed(self, res):
        pass

    def parse(self, response):
        body = response.body
        url = response.url
        hxf = Selector(text=body)

        items = hxf.xpath('//div[@class="main-left"]/div[@class="List"]/ul/li')
        with open(self.file_path + self.file_name, 'a') as f:
            for dom in items:
                title = self.common_util.get_extract(dom.xpath('a/text()'))
                on_click = self.common_util.get_extract(dom.xpath('a/@onclick'))

                code = re.search(r"checkUserPower\('(.+)'\);", on_click).group(1)
                detail_url = self.base_detail_url.format(code=code)
                f.write(title + ': ' + detail_url + '\n')
                self.now_item_num += 1

        # 下一页
        total = self.common_util.get_extract(hxf.xpath('//div[@class="page"]/b[1]/text()'))
        if self.now_item_num < int(total):
            this_page_num = int(re.search(r'.+&page=(\d+)', url).group(1))
            yield scrapy.FormRequest(url=self.base_url.format(page=this_page_num + 1), method='GET')
