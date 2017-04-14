"""
网易云音乐 常量
"""
from thor_crawl.utils.constant.constant import Constant


class M163Constant:
    # =========================== 请求相关 ===========================
    HEADERS = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip,deflate,sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'music.163.com',
        'Referer': 'http://music.163.com/search/',
        'User-Agent': Constant.UA_GROUP[0]
    }

    COOKIES = {
        'appver': '1.5.2'
    }
