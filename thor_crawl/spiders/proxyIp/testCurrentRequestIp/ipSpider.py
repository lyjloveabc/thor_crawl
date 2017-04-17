"""
测试当前请求的IP（主要是想看看代理IP是否有效）
http://www.ip.cn/
"""
from scrapy import Selector
from scrapy.spiders import Spider

from thor_crawl.utils.commonUtil import CommonUtil
from thor_crawl.utils.db.daoUtil import DaoUtils


class IpSpider(Spider):
    name = 'proxyIp_testCurrentRequestIp_ip138Spider'
    handle_httpstatus_list = [301, 302, 204, 206, 404, 500]

    start_urls = ['http://www.ip.cn/']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ============ 工具 ============
        self.dao = DaoUtils()
        self.common_util = CommonUtil()

    def __del__(self):
        pass

    def closed(self, res):
        pass

    def parse(self, response):
        body = response.body
        hxf = Selector(text=body)

        result_div = hxf.xpath('//div[@id="result"]/div')
        ip = self.common_util.get_extract(result_div.xpath('p[1]/code/text()'))
        address = self.common_util.get_extract(result_div.xpath('p[2]/code/text()'))
        geo_ip = self.common_util.get_extract(result_div.xpath('p[3]/text()'))

        print('ip:', ip)
        print('address:', address)
        print('geo_ip:', geo_ip)
