# coding=utf-8
import random
import time

import requests.packages.urllib3.util.ssl_
from scrapy import Selector


class CityZoneDetail:
    def __init__(self):
        self.update_sql = 'UPDATE fang_city_zone_new SET land_area = "{land_area}", building_area = "{building_area}", property_fee = "{property_fee}" WHERE id = {id};'
        self.value = 50
        self.value_2 = 5000

        self.UA_GROUP = [
            # ************************************ START 新加 ************************************ #
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36'
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:52.0) Gecko/20100101 Firefox/52.0',
            # ************************************ END 新加 ************************************ #

            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6',
            'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6',
            'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1',
            'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3',
            'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3',
            'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3',
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3',
            'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3',
            'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24'
        ]

    def __del__(self):
        CityZoneDetail.say(content="张莹老婆快来救救我啊", circle_num=2)

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
        print(file_name.replace('file/zone_url_', '').replace('.txt', ''))
        CityZoneDetail.say("现在开始处理第" + file_name.replace('file/zone_url_', '').replace('.txt', '') + "个文件")
        db_data = CityZoneDetail.read_data(file_name)
        print("db_data: " + str(len(db_data)))

        index = 0
        need_update = list()
        for row in db_data:
            index += 1
            print(index, row)
            if index % self.value_2 == 0:
                CityZoneDetail.say("index是" + str(index) + "，要暂停120秒了")
                time.sleep(120)
                CityZoneDetail.say("暂停120秒结束，继续开始")
            if index % self.value == 0 and index % self.value_2 != 0:
                CityZoneDetail.say("index是" + str(index) + "，要暂停2秒了")
                time.sleep(2)
                CityZoneDetail.say("暂停2秒结束，继续开始")

            try:
                requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'
                response = requests.get('https:' + row['du'], headers={'User-Agent': random.choice(self.UA_GROUP)}, timeout=10)
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
                if CityZoneDetail.get_extract(field.xpath('strong/text()')) == '占地面积：':
                    land_area = CityZoneDetail.get_extract(field.xpath('text()'))
                if CityZoneDetail.get_extract(field.xpath('strong/text()')) == '建筑面积：':
                    building_area = CityZoneDetail.get_extract(field.xpath('text()'))
                if CityZoneDetail.get_extract(field.xpath('strong/text()')) == '物 业 费：':
                    property_fee = CityZoneDetail.get_extract(field.xpath('text()'))
            need_update.append(
                self.update_sql.format(land_area=land_area, building_area=building_area, property_fee=property_fee, id=row['id'])
            )
        with open(file_name.replace('.txt', '') + '_out.txt', 'a') as f:
            for row in need_update:
                f.write(row + '\n')
        CityZoneDetail.say("第" + file_name.replace('file/zone_url_', '').replace('.txt', '') + "个文件处理完毕！")

    ####
    @staticmethod
    def get_extract(xpath_site, is_only=True):
        """ 当取出的长度大于0, 取出其值. isOnly True; 只取第一个. False:取所有. """
        extract_group = xpath_site.extract()
        if len(extract_group) > 0:
            if is_only:
                return extract_group[0].strip()
            else:
                return extract_group
        return ''

    @staticmethod
    def say(content="主人救命啊！", circle_num=1):
        for n in range(0, circle_num):
            if n > 0:
                time.sleep(10)
            print(content)


if __name__ == '__main__':
    czd = CityZoneDetail()
    # czd.handle('file/zone_url_1.txt')
    # CityZoneDetail.say("等待两分钟")
    # time.sleep(120)
    # czd.handle('file/zone_url_2.txt')
    # CityZoneDetail.say("等待两分钟")
    # time.sleep(120)
    czd.handle('file/zone_url_3.txt')
    # CityZoneDetail.say("等待两分钟")
    # time.sleep(120)
    # czd.handle('file/zone_url_4.txt')
