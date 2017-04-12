"""
http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2015/index.html
2015年统计用区划代码和城乡划分代码(截止2015年09月30日)
"""
import scrapy
from scrapy import Selector
from scrapy.spiders import BaseSpider

from thor_crawl.utils.commonUtil import CommonUtil
from thor_crawl.utils.db.daoUtil import DaoUtils


class ChineseRegion(BaseSpider):
    name = 'statistical_stats_chineseRegion'
    handle_httpstatus_list = [301, 302, 204, 206, 404, 500]

    start_urls = ['http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2015/index.html']

    def __init__(self):
        # ============ 工具 ============
        self.dao = DaoUtils()
        self.common_util = CommonUtil()

        # ============ 持久化相关变量定义 ============
        self.save_threshold = 1000
        self.persistent_data = list()
        self.main_table = 'chinese_region'
        self.base_url_format = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2015/{sub}'

    def __del__(self):
        pass
        #self.save_final()

    def closed(self, res):
        pass
        #self.save_final()

    def parse(self, response):
        body = response.body.decode('gb2312')
        meta = response.meta
        hxf = Selector(text=body)

        province_tr = hxf.xpath('//table[@class="provincetable"]/tr[@class="provincetr"]')
        for province_list in province_tr:
            province_td = province_list.xpath('td')
            for province in province_td:
                province_sub = self.common_util.get_extract(province.xpath('a/@href'))
                province_name = self.common_util.get_extract(province.xpath('a/text()'))

                yield scrapy.FormRequest(url=self.base_url_format.format(sub=province_sub), method='GET', meta=meta)
                print(self.common_util.get_extract(province.xpath('a/@href')))
                print(self.common_util.get_extract(province.xpath('a/text()')))

            # code = self.common_util.get_extract(fund_item.xpath('td[1]/text()'))
            # simple_name = self.common_util.get_extract(fund_item.xpath('td[2]/a/text()'))
            # latest_net_value = self.common_util.get_extract(fund_item.xpath('td[3]/p[1]/text()'))
            # latest_net_value_date = self.common_util.get_extract(fund_item.xpath('td[3]/p[2]/text()'))
            # day_of_growth = self.common_util.get_extract(fund_item.xpath('td[4]/span/text()'))
            # nearly_a_month = self.common_util.get_extract(fund_item.xpath('td[5]/span/text()'))
            # nearly_three_months = self.common_util.get_extract(fund_item.xpath('td[6]/span/text()'))
            # almost_a_year = self.common_util.get_extract(fund_item.xpath('td[7]/span/text()'))
            # since_this_year = self.common_util.get_extract(fund_item.xpath('td[8]/span/text()'))
            # since_set_up = self.common_util.get_extract(fund_item.xpath('td[9]/span/text()'))
            # investment_amount_threshold = self.common_util.get_extract(fund_item.xpath('td[10]/text()'))
            # lu_fund = {
            #     'code': code,
            #     'simple_name': simple_name,
            #     'latest_net_value': latest_net_value,
            #     'latest_net_value_date': latest_net_value_date,
            #     'day_of_growth': day_of_growth,
            #     'nearly_a_month': nearly_a_month,
            #     'nearly_three_months': nearly_three_months,
            #     'almost_a_year': almost_a_year,
            #     'since_this_year': since_this_year,
            #     'since_set_up': since_set_up,
            #     'investment_amount_threshold': investment_amount_threshold
            # }
            # self.persistent_data.append(lu_fund)

        # self.save()

        # 下一页
        # page_num_text = self.common_util.get_extract(hxf.xpath('//div[@class="pagination-inner"]/p[@class="pageNum"]/text()'))
        # page_nums = re.search(r'第(\d+)页/共(\d+)页', page_num_text)
        # this_page_num = int(page_nums.group(1))
        # total_page_num = int(page_nums.group(2))
        # if this_page_num < total_page_num:
        #     next_page_url = self.base_url_format.format(current_page=this_page_num + 1)
        #     yield scrapy.FormRequest(url=next_page_url, method='GET', meta=meta)

    def save(self):
        if len(self.persistent_data) > self.save_threshold:
            try:
                self.dao.customizable_add_batch(self.main_table, self.persistent_data)
            except AttributeError as e:
                self.dao = DaoUtils()
                self.dao.customizable_add_batch(self.main_table, self.persistent_data)
                print('save except:', e)
            finally:
                self.persistent_data = list()

    def save_final(self):
        if len(self.persistent_data) > 0:
            try:
                self.dao.customizable_add_batch(self.main_table, self.persistent_data)
            except AttributeError as e:
                self.dao = DaoUtils()
                self.dao.customizable_add_batch(self.main_table, self.persistent_data)
                print('save_final except:', e)
            finally:
                self.persistent_data = list()
