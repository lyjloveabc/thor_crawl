"""
电影天堂
"""
from datetime import datetime

import re
import scrapy
from scrapy import Selector
from scrapy.spiders import BaseSpider

from thor_crawl.utils.commonUtil import CommonUtil
from thor_crawl.utils.db.daoUtil import DaoUtils


class NewBoutiqueSpider(BaseSpider):
    name = 'movie_dytt8_new_boutique'
    handle_httpstatus_list = [204, 206, 301, 302, 404, 500]

    start_urls = [
        'http://www.ygdy8.net/html/gndy/dyzz/index.html'
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
        self.base_url = 'http://www.cbia.com.cn/index.php/Home/Infoforum/foruminfolist/code/AT1451369962448R?&page={page}'
        self.base_detail_url = 'http://www.cbia.com.cn/index.php/Home/Infoforum/infodetail/code/{code}'
        self.file_name = '中国轴承行业网_' + '通知' + '_' + self.now_day + '.txt'
        self.file_path = 'spiders/bearing/cbia/file/'

    def __del__(self):
        pass

    def closed(self, res):
        pass

    def parse(self, response):
        body = response.body
        url = response.url
        hxf = Selector(text=body)

        items = hxf.xpath('//div[@class="co_content8"]/ul/td/table')
        for item in items:
            item.xpath('tr[2]/td[2]/')


        # 下一页
        total = self.common_util.get_extract(hxf.xpath('//div[@class="page"]/b[1]/text()'))
        if self.now_item_num < int(total):
            this_page_num = int(re.search(r'.+&page=(\d+)', url).group(1))
            yield scrapy.FormRequest(url=self.base_url.format(page=this_page_num + 1), method='GET')
