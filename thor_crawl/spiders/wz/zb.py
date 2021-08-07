"""
电影天堂 最新电影
http://www.dy2018.com/html/gndy/dyzz/index_2.html
"""
import json
import logging

import scrapy
from scrapy.spiders import Spider

from thor_crawl.spiders.wz.header import HEADERS
from thor_crawl.utils.commonUtil import CommonUtil
from thor_crawl.utils.constant.constant import Constant
from thor_crawl.utils.db.daoUtil import DaoUtils


class Zb(Spider):
    name = 'wx_zb'
    handle_httpstatus_list = [204, 206, 301, 302, 404, 500]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logging.info(Constant.SPIDER_INIT)

        # ============ 工具 ============
        self.dao = DaoUtils()
        self.common_util = CommonUtil()

        # ============ 持久化 ============
        self.save_threshold = 100
        self.main_table = 'wz_zb'
        self.persistent_data = list()

        # ============ 直播间 ============
        self.cId = '119558'
        self.liveId = '97286445'
        self.zbid = '97286445',

        self.sum = 0

    def __del__(self):
        logging.info(Constant.SPIDER_CLOSED)
        self.save_final()

    def start_requests(self):
        start_requests = list()

        start_requests.append(scrapy.FormRequest(
            url='https://dtapi.vzan.com/dtapi/VZLive/GetTopicList',
            method='POST',
            headers=HEADERS,
            formdata=self.live_room(),
            meta={'curr': 1}
        ))

        return start_requests

    def closed(self, res):
        logging.info(Constant.SPIDER_CLOSED)
        # self.save_final()
        print(self.sum)

    def parse(self, response):
        text = response.text
        meta = response.meta

        json_data = json.loads(text)
        # print('===============', str(json_data))

        for row in json_data['dataObj']:
            yield scrapy.FormRequest(url='https://ds.vzan.com/livesapi/gettopicdetail', method='POST', formdata=self.live_detail(row['Id']), callback=self.parse_detail, meta=row)

        if len(json_data['dataObj']) > 0:
            curr = int(meta['curr']) + 1
            yield scrapy.FormRequest(
                url='https://dtapi.vzan.com/dtapi/VZLive/GetTopicList',
                method='POST',
                headers=HEADERS,
                formdata=self.live_room(curr),
                meta={'curr': curr}
            )

        self.save()

    def parse_detail(self, response):
        text = response.text
        json_data = json.loads(text)

        meta = response.meta

        # print('===============', str(json_data))

        data_obj = json_data['dataObj']
        tvurl = data_obj['topic']['tvurl']

        self.sum += 1

        self.persistent_data.append(
            {
                't_id': meta['Id'],
                'c_id': meta['cId'],
                'zb_id': meta['zbId'],
                'title': str(meta['title']),
                'start_time': meta['starttime'],
                'add_time': meta['addtime'],
                'cover': meta['cover'],
                'tv_url': tvurl
            }
        )

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

    def live_room(self, curr=1):
        return {
            'cId': str(self.cId),
            'curr': str(curr),
            'liveId': str(self.liveId),
            'region': 'vzanlive',
            'uid': '1665A5568860ED273FB46B583CB367B7',
            'zbid': str(self.zbid),
            'mbid': '75999',
            'thirdid': '8092962'
        }

    def live_detail(self, tid):
        return {
            'tid': str(tid),
            'stamp': '0',
            'region': 'vzanlive',
            'uid': '1665A5568860ED273FB46B583CB367B7',
            'zbid': str(self.zbid),
            'mbid': '75999',
            'thirdid': '8092962'
        }
