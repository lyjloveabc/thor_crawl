"""
UA 中间件
"""

import random
from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware

from thor_crawl.utils.constant.constant import Constant


class MyUserAgentMiddleware(UserAgentMiddleware):
    def __init__(self, user_agent=''):
        super().__init__(user_agent)
        self.user_agent = user_agent

    def process_request(self, request, spider):
        ua = random.choice(Constant.UA_GROUP)
        if ua:
            request.headers.setdefault('User-Agent', ua)
