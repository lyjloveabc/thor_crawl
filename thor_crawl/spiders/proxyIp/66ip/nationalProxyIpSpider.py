"""
66免费代理网
http://www.66ip.cn/
"""
import logging

import scrapy
from scrapy import Selector
from scrapy.spiders import Spider

from thor_crawl.spiders.proxyIp.proxyIpConstant import ProxyIpConstant
from thor_crawl.utils.constant.constant import Constant

from thor_crawl.utils.commonUtil import CommonUtil
from thor_crawl.utils.db.daoUtil import DaoUtils


class NationalProxyIpSpider(Spider):
    name = 'proxyIp_66ip_nationalProxyIp'
    handle_httpstatus_list = [301, 302, 204, 206, 404, 500]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logging.info(Constant.SPIDER_INIT)

        # ============ 工具 ============
        self.dao = DaoUtils()
        self.common_util = CommonUtil()

        # 参数
        self.base_url = 'http://www.66ip.cn/{page_num}.html'

        # 持久化
        self.source = '66免费代理网'
        self.main_table = 'proxy_ip'
        self.save_threshold = 100
        self.persistent_data = list()

    def __del__(self):
        logging.info(Constant.SPIDER_DEL)
        self.save_final()

    def start_requests(self):
        start_requests = list()

        url = 'http://www.66ip.cn/1.html'
        meta = {'page_num': 1}

        form_request = scrapy.FormRequest(url=url, method='GET', meta=meta)
        start_requests.append(form_request)

        return start_requests

    def closed(self, res):
        logging.info(Constant.SPIDER_CLOSED)
        self.save_final()

    def parse(self, response):
        text = response.text
        hxf = Selector(text=text)
        meta = response.meta

        center = hxf.xpath('//div[@id="main"]/div/div[1]/table/tr')
        for item in center[1:]:
            proxy_id = {
                'ip': self.common_util.get_extract(item.xpath('td[1]/text()')),
                'port': self.common_util.get_extract(item.xpath('td[2]/text()')),
                'address': self.common_util.get_extract(item.xpath('td[3]/text()')),
                'type': ProxyIpConstant.PROXY_IP_TYPE[self.common_util.get_extract(item.xpath('td[4]/text()'))],
                'check_time': self.common_util.get_extract(item.xpath('td[5]/text()')),
                'source': self.source,
            }
            self.persistent_data.append(proxy_id)

        # 下一页
        my_page = hxf.xpath('//div[@id="PageList"]/a')
        last_a_class = self.common_util.get_extract(my_page[-1].xpath('@class'))
        if last_a_class != 'pageCurrent':
            current_page_num = meta['page_num']
            next_page_num = current_page_num + 1
            next_url = self.base_url.format(page_num=next_page_num)
            meta['page_num'] = next_page_num
            yield scrapy.FormRequest(url=next_url, method='GET', meta=meta)

        self.save()

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


if __name__ == '__main__':
    logging.info(NationalProxyIpSpider)
