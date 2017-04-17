"""
中国轴承行业网 VIP才可见的文章
"""
import re
from datetime import datetime

import scrapy
from scrapy import Selector
from scrapy.spiders import Spider

from thor_crawl.utils.commonUtil import CommonUtil
from thor_crawl.utils.db.daoUtil import DaoUtils


class VipDocSpider(Spider):
    name = 'bearing_cbia_vip_doc'
    handle_httpstatus_list = [301, 302, 204, 206, 404, 500]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ============ 工具 ============
        self.dao = DaoUtils()
        self.common_util = CommonUtil()

        # ============ 持久化相关变量定义 ============
        self.save_threshold = 1000
        self.persistent_data = list()
        self.now_day = datetime.today().strftime('%Y%m%d')
        self.now_item_num = 0
        self.base_detail_url = 'http://www.cbia.com.cn/index.php/Home/Infoforum/infodetail/code/{code}'
        self.file_name = '中国轴承行业网_' + 'VIP才可见的文章' + '_' + self.now_day + '.txt'
        self.file_path = 'spiders/bearing/cbia/file/'
        self.domain_name = 'http://www.cbia.com.cn/'

    def __del__(self):
        pass

    def start_requests(self):
        start_requests = set()
        with open(self.file_path + '中国轴承行业网_VIP_20170313.txt') as f:
            for line in f.readlines():
                url = self.domain_name + line[:-1].split(': ')[1] + '?&page=1'
                form_request = scrapy.FormRequest(url=url, method='GET')
                start_requests.add(form_request)
        print(start_requests)
        return start_requests

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
            next_page_url = re.sub(r'&page=(\d+)', '&page=' + str(this_page_num + 1), url)
            yield scrapy.FormRequest(url=next_page_url, method='GET')
