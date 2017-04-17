"""
中国轴承行业网 VIP才可见的项目的初始URL
"""
from datetime import datetime

from scrapy import Selector
from scrapy.spiders import Spider

from thor_crawl.utils.commonUtil import CommonUtil
from thor_crawl.utils.db.daoUtil import DaoUtils


class VipItemUrlSpider(Spider):
    name = 'bearing_cbia_vip_item_url'
    handle_httpstatus_list = [301, 302, 204, 206, 404, 500]

    start_urls = [
        'http://www.cbia.com.cn/index.php/Home/Infoforum/foruminfolist/code/AT1451369946MAWF?&page=1'
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ============ 工具 ============
        self.dao = DaoUtils()
        self.common_util = CommonUtil()

        # ============ 持久化相关变量定义 ============
        self.save_threshold = 1000
        self.persistent_data = list()
        self.now_day = datetime.today().strftime('%Y%m%d')
        self.file_name = '中国轴承行业网_' + 'VIP' + '_' + self.now_day + '.txt'
        self.file_path = 'spiders/bearing/cbia/file/'

    def __del__(self):
        pass

    def closed(self, res):
        pass

    def parse(self, response):
        body = response.body
        hxf = Selector(text=body)

        items = hxf.xpath('//div[@class="navList"]/div[3]/ul/li')
        with open(self.file_path + self.file_name, 'a') as f:
            for dom in items:
                title = self.common_util.get_extract(dom.xpath('a/text()'))
                vip_item_url = self.common_util.get_extract(dom.xpath('a/@href'))

                f.write(title + ': ' + vip_item_url + '\n')
