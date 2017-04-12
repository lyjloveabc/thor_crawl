# http://kg2.qq.com/share.html?s=y44q9JAoOARS&songid=1100008486
# http://kg.qq.com/
import json

from scrapy.spiders import BaseSpider

from scrapy import Selector


class Kg(BaseSpider):
    name = 'music_qmkg_kg'
    handle_httpstatus_list = [404]
    start_urls = {
        'http://cgi.kg.qq.com/fcgi-bin/kg_ugc_get_homepage?jsonpCallback=callback_0&inCharset=GB2312&outCharset=utf-8&format='
        '&g_tk=1911569177&g_tk_openkey=1911569177&nocache=0.023400110540915398'
        '&type=get_uinfo&start=1&num=8&touin=&share_uid=63989e842128328c36&_=1482150988164'
    }

    def __init__(self):
        pass

    # http://kg.qq.com/personal.html?uid=63989e842128328c36
    def parse(self, response):
        hxf = Selector(response)
        meta = response.meta

        json.load(response.body)
        print()

