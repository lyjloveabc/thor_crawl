"""
电影天堂 最新电影
http://www.dy2018.com/html/gndy/dyzz/index_2.html
"""
import json
import re
import logging

import requests
import scrapy
from scrapy import Selector
from scrapy.spiders import Spider

from thor_crawl.utils.commonUtil import CommonUtil
from thor_crawl.utils.constant.constant import Constant
from thor_crawl.utils.db.daoUtil import DaoUtils


class Db(Spider):
    name = 'db_d'
    handle_httpstatus_list = [204, 206, 301, 302, 404, 500]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logging.info(Constant.SPIDER_INIT)

        # ============ 工具 ============
        self.dao = DaoUtils()
        self.common_util = CommonUtil()

        self.domain = 'https://www.douban.com'
        self.base_url = 'https://www.douban.com/group/topic/90323810/?start={start}'
        self.remove_base_url = 'https://www.douban.com/j/group/topic/90323810/remove_comment'
        self.referer_base = 'https://www.douban.com/group/topic/{cid}/'

        self.headers = {
            'Host': 'www.douban.com',
            'Connection': 'keep-alive',
            'Content-Length': '22',
            'Accept': 'text/plain,*/*;q=0.01',
            'Origin': 'https://www.douban.com',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0(Macintosh;IntelMacOSX10_13_6)AppleWebKit/537.36(KHTML,likeGecko)Chrome/69.0.3497.81Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://www.douban.com/group/topic/90323810/',
            'Accept-Encoding': 'gzip,deflate,br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }
        self.cookies = {
            'bid': '442OKudequU',
            'douban-fav-remind': '1',
            '__yadk_uid': 'QLsssUg0OHNS05ggccpyGOkrzlR87vRu',
            'll': '"118172"',
            '_vwo_uuid_v2': 'D999E75B6520205D5493F9E3CBE7EA81A|96a7288963b0c22d4b3a79f944e268ed',
            '_ga': 'GA1.2.444907684.1535806542',
            'push_noty_num': '0',
            'push_doumail_num': '0',
            '__utmv': '30149280.6600',
            'douban-profile-remind': '1',
            'ct': 'y',
            'ps': 'y',
            '__utmz': '30149280.1536634835.6.3.utmcsr=baidu|utmccn=(organic)|utmcmd=organic',
            '_pk_ref.100001.8cb4': '%5B%22%22%2C%22%22%2C1536717893%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DgLb055XFNzEK3HvCb4tWVIHxgcEMW7tE1Kdh6hSFvZpHVbfjIEzBVo59OM1iQQAH%26wd%3D%26eqid%3D8fe1cdae00017154000000045b972fc3%22%5D',
            '_pk_ses.100001.8cb4': '*',
            'ap_v': '0,6.0',
            '__utma': '30149280.444907684.1535806542.1536634835.1536717895.7',
            '__utmc': '30149280',
            'dbcl2': '"66002721:cLJ0U+SObDQ"',
            'ck': 'KRq5',
            '__utmt': '1',
            '__utmb': '30149280.500.8.1536718676470',
            '_pk_id.100001.8cb4': '4b18d8548e2018fd.1535806541.7.1536719018.1536634843.',
        }

    def __del__(self):
        logging.info(Constant.SPIDER_CLOSED)

    def start_requests(self):
        start_requests = list()

        meta = {'start': 0}
        form_request = scrapy.FormRequest(url=self.base_url.format(start=0), method='GET', meta=meta)
        start_requests.append(form_request)

        return start_requests

    def closed(self, res):
        logging.info(Constant.SPIDER_CLOSED)

    def parse(self, response):
        text = response.text
        hxf = Selector(text=text)
        meta = response.meta

        print('hehe:', hehe)

        comments = hxf.xpath('//ul[@id="comments"]/li')
        for item in comments:
            text_temp = self.common_util.get_extract(item.xpath('div[2]/div[1]/h4/a/text()'))
            if text_temp == 'Thor':
                # db-global-nav
                print('Thor: ', response.url)
                param = {
                    'cid': self.common_util.get_extract(item.xpath('@id')),
                    'ck': 'znM_'
                }
                r = requests.post(self.remove_base_url, data=param, headers=self.headers, cookies=self.cookies)
                print(r)

        # 下一页
        next_page_url = self.common_util.get_extract(hxf.xpath('//div[@class="paginator"]/span[@class="next"]/a/@href'))
        if next_page_url is not None and next_page_url != '':
            yield scrapy.FormRequest(url=next_page_url, method='GET', meta=meta)
