from scrapy import Selector
from scrapy.spiders import Spider

from thor_crawl.spiders.spider_setting import DEFAULT_DB_ENV
from thor_crawl.utils.commonUtil import CommonUtil
from thor_crawl.utils.db.daoUtil import DaoUtils


class City(Spider):
    name = 'fang_city'
    handle_httpstatus_list = [204, 206, 404, 500]

    start_urls = ['https://www.fang.com/SoufunFamily.htm']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ============ 工具 ============
        self.dao = DEFAULT_DB_ENV
        self.common_util = CommonUtil()

        # ============ 持久化相关变量定义 ============
        self.save_threshold = 20  # 一次性插入数据库阈值
        self.persistent_data = list()  # 内存暂存处理的数据，批量插入数据库
        self.main_table = 'fang_city'  # 数据库存储表

    def __del__(self):
        self.save_final()

    def closed(self, res):
        self.save_final()

    def parse(self, response):
        try:
            body = response.body.decode('gb18030').encode('utf-8')
        except UnicodeDecodeError as e:
            print(e)
            body = response.body
        hxf = Selector(text=body)

        trs = hxf.xpath('//div[@id="c02"]/table/tr')  # 获取所有的行数据
        this_province = '未知'

        for tr in trs[:-1]:
            province_name = self.common_util.get_extract(tr.xpath('td[2]/strong/text()'))  # 获取省份名称文本值
            this_province = this_province if province_name is None or province_name == '' else province_name  # 为空的话取之前的省份名称

            cities = tr.xpath('td[3]/a')  # 获取所有的城市列表
            for city in cities:
                city_name = self.common_util.get_extract(city.xpath('text()'))  # 获取城市名称文本值
                city_index_url = self.common_util.get_extract(city.xpath('@href'))  # 获取城市首页链接
                self.persistent_data.append(
                    {
                        'province_name': this_province,
                        'city_name': city_name,
                        'city_index_url': city_index_url
                    }
                )
        self.save()

    def save(self):
        if len(self.persistent_data) > self.save_threshold:
            try:
                self.dao.customizable_add_ignore_batch(self.main_table, self.persistent_data, time=False)
            except AttributeError as e:
                self.dao = DaoUtils()
                self.dao.customizable_add_ignore_batch(self.main_table, self.persistent_data, time=False)
                print('save except:', e)
            finally:
                self.persistent_data = list()

    def save_final(self):
        if len(self.persistent_data) > 0:
            try:
                self.dao.customizable_add_ignore_batch(self.main_table, self.persistent_data, time=False)
            except AttributeError as e:
                self.dao = DaoUtils()
                self.dao.customizable_add_ignore_batch(self.main_table, self.persistent_data, time=False)
                print('save_final except:', e)
            finally:
                self.persistent_data = list()
