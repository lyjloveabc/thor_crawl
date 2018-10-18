"""
https://www.douban.com/group/people/66002721/reply
"""
import logging
import re

import requests
import scrapy
from scrapy import Selector
from scrapy.spiders import Spider

from thor_crawl.utils.commonUtil import CommonUtil
from thor_crawl.utils.constant.constant import Constant
from thor_crawl.utils.db.daoUtil import DaoUtils


class Reply(Spider):
    name = 'db_reply'
    handle_httpstatus_list = [204, 206, 301, 302, 404, 500]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logging.info(Constant.SPIDER_INIT)

        # ============ 工具 ============
        self.dao = DaoUtils()
        self.common_util = CommonUtil()

        self.domain = 'https://www.douban.com'
        self.reply = 'https://www.douban.com/group/people/66002721/reply'

        self.topic_url = 'https://www.douban.com/group/topic/{topic_id}/'
        self.remove_base_url = 'https://www.douban.com/j/group/topic/{topic_id}/remove_comment'
        self.referer_base = 'https://www.douban.com/group/topic/{topic_id}/'

        self.headers_reply = {
            'Host': 'www.douban.com',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0(Macintosh;IntelMacOSX10_13_6)AppleWebKit/537.36(KHTML,likeGecko)Chrome/69.0.3497.81Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip,deflate,br',
            'Accept-Language': 'zh-CN,zh;q=0.9',

        }
        self.headers_topic = {
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
            '__utmc': '30149280',
            '_pk_ref.100001.8cb4': '%5B%22%22%2C%22%22%2C1536727259%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DgLb055XFNzEK3HvCb4tWVIHxgcEMW7tE1Kdh6hSFvZpHVbfjIEzBVo59OM1iQQAH%26wd%3D%26eqid%3D8fe1cdae00017154000000045b972fc3%22%5D',
            '_pk_ses.100001.8cb4': '*',
            'dbcl2': '"66002721:Ozh956sPdmo"',
            '_gid': 'GA1.2.1040788658.1536727261',
            'ck': 'fTYl',
            'ap_v': '0,6.0',
            '__utma': '30149280.444907684.1535806542.1536717895.1536727265.8',
            '_pk_id.100001.8cb4': '4b18d8548e2018fd.1535806541.8.1536727775.1536722971.',
            '__utmb': '30149280.14.10.1536727265',
            '__utmt': '1',
        }

    def __del__(self):
        logging.info(Constant.SPIDER_CLOSED)

    def start_requests(self):
        start_requests = list()

        meta = {}
        form_request = scrapy.FormRequest(url=self.reply, method='GET', meta=meta, headers=self.headers_reply, cookies=self.cookies)
        start_requests.append(form_request)

        return start_requests

    def closed(self, res):
        logging.info(Constant.SPIDER_CLOSED)

    def parse(self, response):
        text = response.text
        hxf = Selector(text=text)
        meta = response.meta

        trs = hxf.xpath('//table[@class="olt"]/tr')
        a = [trs[0]]
        for item in a:
            href = self.common_util.get_extract(item.xpath('td[1]/a/@href'))
            if href is not None and href != '':
                # 获得话题ID
                topic_id = re.search(r'https://www.douban.com/group/topic/(\d+)/', href).group(1)
                meta['topic_id'] = topic_id
                self.headers_topic['Referer'] = self.referer_base.format(topic_id=topic_id)
                yield scrapy.FormRequest(url=self.topic_url.format(topic_id=topic_id), method='GET',
                                         meta=meta, headers=self.headers_topic, cookies=self.cookies, callback=self.parse_topic)

        # 下一页
        next_page_url = self.common_util.get_extract(hxf.xpath('//div[@class="paginator"]/span[@class="next"]/a/@href'))
        if next_page_url is not None and next_page_url != '':
            yield scrapy.FormRequest(url=self.domain + next_page_url, method='GET', meta=meta, headers=self.headers_reply, cookies=self.cookies)

    def parse_topic(self, response):
        text = response.text
        hxf = Selector(text=text)
        meta = response.meta

        comments = hxf.xpath('//ul[@id="comments"]/li')
        for item in comments:
            text_temp = self.common_util.get_extract(item.xpath('div[2]/div[1]/h4/a/text()'))
            if text_temp == 'Thor':
                param = {
                    'cid': self.common_util.get_extract(item.xpath('@id')),
                    'ck': meta['ck']
                }
                r = requests.post(self.remove_base_url, data=param, headers=self.headers_topic, cookies=self.cookies)
                print('remove:', r)

        # 下一页
        next_page_url = self.common_util.get_extract(hxf.xpath('//div[@class="paginator"]/span[@class="next"]/a/@href'))
        if next_page_url is not None and next_page_url != '':
            yield scrapy.FormRequest(url=next_page_url, method='GET', meta=meta)
