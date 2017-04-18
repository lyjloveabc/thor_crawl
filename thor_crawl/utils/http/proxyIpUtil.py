"""
代理IP, 处理工具
"""
import logging
import requests

from requests import RequestException

logging.basicConfig()
logger = logging.getLogger(__name__)


class ProxyIpUtil:
    __REQUEST_URL = 'http://www.w3school.com.cn/index.html'
    __TIME_OUT = 2

    def __init__(self):
        pass

    # 判断一个代理IP是否有效, 入参是dict
    @staticmethod
    def is_effective(ip_type, proxy_ip):
        result = False
        try:
            proxies = {ip_type: proxy_ip}

            response = requests.get(url=ProxyIpUtil.__REQUEST_URL, proxies=proxies, timeout=ProxyIpUtil.__TIME_OUT)
            if response.status_code == 200:
                result = True
        except RequestException as error:
            print(error)
        finally:
            return result


if __name__ == '__main__':
    ProxyIpUtil().is_effective('http', 'http://192.168.1.101:80')
