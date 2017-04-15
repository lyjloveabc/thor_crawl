"""
代理IP 中间件
"""
import logging

from datetime import datetime, timedelta
from twisted.internet.error import TimeoutError, ConnectionRefusedError, ConnectError

from thor_crawl.utils.constant.constant import Constant

from thor_crawl.utils.commonUtil import CommonUtil
from thor_crawl.utils.db.daoUtil import DaoUtils

__author__ = 'lyj'

logger = logging.getLogger(__name__)


class ProxyMiddleware(object):
    # 遇到这些类型的错误直接当做代理不可用处理掉
    REQUEST_ERRORS = (TimeoutError, ConnectionRefusedError, ConnectError, ValueError)

    __DB_TABLE_MAIN = 'proxy_ip'

    def __init__(self):
        # ============ 工具 ============
        self.dao = DaoUtils()
        self.common_util = CommonUtil()

        # ============ 参数 ============
        self.switching_time_point = datetime.now()  # 代理和非代理的切换时间点
        self.last_proxy_index = 0  # 保存上次使用的是哪个代理(代理池的下标)
        self.proxy_interval = 60  # 一定秒数后切换回不用代理(这个一定秒数, 就是代理模式的运行时间)
        self.no_proxy_interval = 60  # 一定秒数后切到代理模式(这个一定秒数, 就是不用代理的运行时间)
        self.proxy_index = 0  # 初始时使用0号代理(即无代理)
        self.proxies = [{'proxy': None, 'count': 0}]  # 初始化代理列表
        self.fixed_proxy = len(self.proxies)  # 表示可信代理的数量(如自己搭建的HTTP代理)+1(不用代理直接连接)
        self.proxy_poll_size = 10  # 代理IP池, 大小

        # ============ 数据初始化 ============
        self.expand_proxy_poll_from_db()

    # 将request设置为使用代理
    def process_request(self, request, spider):
        # 有些代理会把请求重定向到一些莫名其妙的地址
        request.meta["dont_redirect"] = True

        # 代理和非代理模式的切换
        # if self.proxy_index > 0 and datetime.now() > (self.switching_time_point + timedelta(minutes=self.proxy_interval)):
        #     logger.info("======F切换到<不使用代理>模式")
        #     self.last_proxy_index = self.proxy_index
        #     self.switching_time_point = datetime.now()
        #     self.proxy_index = 0
        # elif self.proxy_index == 0 and datetime.now() > (self.switching_time_point + timedelta(minutes=self.proxy_interval)):
        #     logger.info("======D切换到<代理>模式")
        #     self.switching_time_point = datetime.now()
        #     self.proxy_index = (self.last_proxy_index + 1) % len(self.proxies)

        if datetime.now() > (self.switching_time_point + timedelta(minutes=self.proxy_interval)):
            self.last_proxy_index = self.proxy_index
            logger.info("======N切换代理")
            logger.info("======oooo" + str(self.proxy_index))
            self.switching_time_point = datetime.now()
            self.proxy_index = (self.proxy_index + 1) % len(self.proxies)

        self.set_proxy(request)

    # 检查response.status, 根据status是否在允许的状态码中决定是否切换到下一个proxy, 或者禁用proxy
    def process_response(self, request, response, spider):
        # 一次请求后, 打印这次请求使用代理的情况
        if "proxy" in request.meta.keys():
            logger.info("======请求的代理情况: %s %s %s" % (request.meta["proxy"], response.status, request.url))
        else:
            logger.info("======请求未用代理: None %s %s" % (response.status, request.url))

        # status不是正常的200, 且不在spider声明的正常爬取过程中可能出现的status列表中, 则认为代理无效, 切换代理
        if response.status != 200 and (not hasattr(spider, "handle_httpstatus_list") or response.status not in spider.handle_httpstatus_list):
            self.invalid_proxy(request.meta["proxy_index"])
            new_request = request.copy()
            return new_request
        else:
            return response

    # 处理由于使用代理导致的连接异常
    def process_exception(self, request, exception, spider):
        if isinstance(exception, self.REQUEST_ERRORS):
            self.invalid_proxy(request.meta["proxy_index"])
            new_request = request.copy()
            return new_request

    # 扩充代理IP池
    def expand_proxy_poll_from_db(self):
        proxy_ip_arr = self.dao.db.get_all_row('select id, ipv4, port, ip_type from ' + ProxyMiddleware.__DB_TABLE_MAIN + ' where is_effective = "Y" and id <2205')
        for proxy_ip in proxy_ip_arr:
            proxy_ip_obj = {
                'proxy': proxy_ip['ip_type'].lower() + '://' + proxy_ip['ipv4'] + ':' + proxy_ip['port'],
                'count': 0
            }
            self.proxies.append(proxy_ip_obj)
        logger.info("======当前代理IP池, 代理IP数量: %d" % (len(self.proxies)))

    # 将request设置不使用代理或使用下一个有效代理
    def set_proxy(self, request):
        proxy = self.proxies[self.proxy_index]
        request.meta["proxy_index"] = self.proxy_index
        proxy["count"] += 1

        if proxy["proxy"]:
            # 使用代理
            request.meta["proxy"] = proxy["proxy"]
        elif "proxy" in request.meta.keys():
            # 不使用代理
            del request.meta["proxy"]

    # 调整当前proxy_index到下一个有效代理的位置, 同时删除无效代理
    def invalid_proxy(self, index):
        self.proxy_index = (self.last_proxy_index + 1) % len(self.proxies)

        if index >= self.fixed_proxy:  # 可信代理
            del self.proxies[index]

        if len(self.proxies) < self.proxy_poll_size:
            self.expand_proxy_poll_from_db()
