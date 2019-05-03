# coding=utf-8
import random
import time

import requests.packages.urllib3.util.ssl_
from scrapy import Selector

from thor_crawl.utils.commonUtil import CommonUtil
from thor_crawl.utils.constant.constant import Constant
from thor_crawl.utils.system.systemUtil import SystemUtil


class CityZoneDetail:
    def __init__(self):
        self.common_util = CommonUtil()
        self.update_sql = 'UPDATE fang_city_zone_new SET land_area = "{land_area}", building_area = "{building_area}", property_fee = "{property_fee}" WHERE id = {id};'
        self.value = 2000
        self.value_2 = 10000

    def __del__(self):
        SystemUtil.say(content="张莹老婆快来救救我啊", circle_num=2)

    @staticmethod
    def read_data(file_name):
        data = list()
        with open(file_name, 'r') as f:
            for row in f.readlines():
                row = row.replace('\n', '')
                row_arr = row.split(',')
                if row_arr[1] != '' and row_arr[1] is not None and not row_arr[1].startswith('/house-xm'):
                    data.append({
                        'id': row_arr[0],
                        'du': row_arr[2]
                    })
        return data

    @staticmethod
    def write_file(source):
        return source.replace('.txt', '') + '_out.txt'

    @staticmethod
    def write_data(file_name, need_update):
        with open(file_name.replace('.txt', '') + '_out.txt', 'a') as f:
            for row in need_update:
                f.write(row + '\n')

    def handle(self, file_name):
        db_data = CityZoneDetail.read_data(file_name)
        print("db_data: " + str(len(db_data)))

        index = 1
        need_update = list()
        for row in db_data[0:10]:
            print(row)
            if index % self.value_2 == 0:
                SystemUtil.say("index是" + str(index) + "，要暂停60秒了")
                time.sleep(60)
                SystemUtil.say("暂停60秒结束，继续开始")
            if index % self.value == 0 and index % self.value_2 != 0:
                SystemUtil.say("index是" + str(index) + "，要暂停10秒了")
                time.sleep(10)
                SystemUtil.say("暂停10秒结束，继续开始")

            try:
                requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'
                response = requests.get('https:' + row['du'], headers={'User-Agent': random.choice(Constant.UA_GROUP)}, timeout=10)
            except Exception as e:
                print(e)
                print('request error: ', row['du'])
                continue
            try:
                text = response.content.decode('gb18030').encode('utf-8')
            except UnicodeDecodeError as e:
                text = response.content

            hxf = Selector(text=text)

            land_area = ''
            building_area = ''
            property_fee = ''
            fields = hxf.xpath('//dl[@class=" clearfix mr30"]/dd')
            for field in fields:
                if self.common_util.get_extract(field.xpath('strong/text()')) == '占地面积：':
                    land_area = self.common_util.get_extract(field.xpath('text()'))
                if self.common_util.get_extract(field.xpath('strong/text()')) == '建筑面积：':
                    building_area = self.common_util.get_extract(field.xpath('text()'))
                if self.common_util.get_extract(field.xpath('strong/text()')) == '物 业 费：':
                    property_fee = self.common_util.get_extract(field.xpath('text()'))
            need_update.append(
                self.update_sql.format(land_area=land_area, building_area=building_area, property_fee=property_fee, id=row['id'])
            )
        with open(file_name.replace('.txt', '') + '_out.txt', 'a') as f:
            for row in need_update:
                f.write(row + '\n')


if __name__ == '__main__':
    czd = CityZoneDetail()
    czd.handle('file/zone_url_1.txt')
