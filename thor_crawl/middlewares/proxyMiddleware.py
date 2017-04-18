"""
代理IP 中间件
"""
import logging

from datetime import datetime, timedelta
from twisted.internet.error import TimeoutError, ConnectionRefusedError, ConnectError

from thor_crawl.utils.commonUtil import CommonUtil
from thor_crawl.utils.db.daoUtil import DaoUtils


class ProxyMiddleware:
    # 遇到这些类型的错误直接当做代理不可用处理掉
    REQUEST_ERRORS = (TimeoutError, ConnectionRefusedError, ConnectError, ValueError)

    __DB_TABLE_MAIN = 'proxy_ip'

    def __init__(self):
        # ============ 工具 ============
        self.dao = DaoUtils()
        self.common_util = CommonUtil()

        # ============ 参数 ============
        self.proxy_poll_min_size = 10  # 代理IP池, 大小
        self.proxies = [{'proxy': None, 'count': 0}]  # 代理池，初始放进去一个代表不使用代理的字典
        self.switch_time_point = datetime.now()  # 代理和非代理的切换时间点，初始化的时候是当前时间
        self.switch_proxy_interval = 3  # 代理切换时间间隔，以秒数记
        self.proxy_index = 1  # 初始时使用0号代理(即不用代理)
        self.last_proxy_index = 0  # 上次使用的代理的下标

        self.fixed_proxy = len(self.proxies)  # 表示可信代理的数量(如自己搭建的HTTP代理)+1(不用代理直接连接)

        # ============ 数据初始化 ============
        self.expand_proxy_poll_from_db()

    # 将request设置为使用代理
    def process_request(self, request, spider):
        # 禁止网页重定
        request.meta['dont_redirect'] = True

        datetime_now = datetime.now()
        current_switch_time_point = self.switch_time_point + timedelta(seconds=self.switch_proxy_interval)

        if datetime_now > current_switch_time_point:
            self.last_proxy_index = self.proxy_index
            self.switch_time_point = datetime_now
            self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
            logging.info('====== {last_proxy_index} 切换 {current_proxy_index}'
                         .format(last_proxy_index=self.last_proxy_index, current_proxy_index=self.proxy_index))

        self.set_proxy(request)

    # 检查response.status, 根据status是否在允许的状态码中决定是否切换到下一个proxy, 或者禁用proxy
    def process_response(self, request, response, spider):
        # 打印响应对应的这次请求使用代理的情况
        if 'proxy' in request.meta.keys():
            logging.info('======process_response 请求的代理情况: {proxy} {status} {url}'
                         .format(proxy=request.meta['proxy'], status=response.status, url=request.url))
        else:
            logging.info('======process_response 请求未使用代理: None {status} {url}'.format(status=response.status, url=request.url))

        if response.status == 200 or not hasattr(spider, 'handle_httpstatus_list'):
            # 响应是200，或者spider对象没有设置handle_httpstatus_list，则不重新发起请求
            return response
        else:
            if response.status in spider.handle_httpstatus_list:
                # 重新发起请求
                self.invalid_proxy(request.meta['proxy_index'])
                new_request = request.copy()
                return new_request
            else:
                return response

    # 处理由于使用代理导致的连接异常
    def process_exception(self, request, exception, spider):
        if 'proxy' in request.meta.keys():
            logging.info('======process_exception 请求的代理情况: {proxy} {url}'.format(proxy=request.meta['proxy'], url=request.url))
        else:
            logging.info('======process_exception 请求未使用代理: None {url}'.format(url=request.url))

        if isinstance(exception, self.REQUEST_ERRORS):
            self.invalid_proxy(request.meta['proxy_index'])
            new_request = request.copy()
            return new_request

    # 扩充代理IP池
    def expand_proxy_poll_from_db(self):
        # proxy_ip_group = self.dao.get_all('select id, ipv4, port, ip_type from ' + ProxyMiddleware.__DB_TABLE_MAIN + ' where is_effective = "Y" and id <2205')
        proxy_ip_group = [
            {'ip_type': 'http', 'ipv4': '180.110.4.78', 'port': '808'},
        ]

        for proxy_ip in proxy_ip_group:
            proxy_ip_dict = {
                'proxy': proxy_ip['ip_type'].lower() + '://' + proxy_ip['ipv4'] + ':' + proxy_ip['port'],
                'count': 0
            }
            self.proxies.append(proxy_ip_dict)

        logging.info('======当前代理IP池代理IP的数量: {proxies}'.format(proxies=len(self.proxies)))

    # 设置代理
    def set_proxy(self, request):
        request.meta['proxy_index'] = self.proxy_index

        proxy = self.proxies[self.proxy_index]
        proxy['count'] += 1

        if proxy['proxy']:
            request.meta['proxy'] = proxy['proxy']  # 使用代理
        else:
            if 'proxy' in request.meta.keys():
                del request.meta['proxy']  # 不使用代理

    # 调整当前proxy_index到下一个有效代理的位置, 同时删除无效代理
    def invalid_proxy(self, index):
        self.proxy_index = (self.last_proxy_index + 1) % len(self.proxies)

        if index >= self.fixed_proxy:  # 可信代理
            del self.proxies[index]

        if len(self.proxies) < self.proxy_poll_min_size:
            self.expand_proxy_poll_from_db()
