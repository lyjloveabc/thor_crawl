"""
created by lyj on 2016/04/22
具体页面爬取器
"""
from scrapy.spiders import Spider

_STANDARD_CODE = 'utf-8'
_PAGE_NAME = 'ygdy8'
_EXTENSION = '.html'
_PAGE_FILE = 'spiders/page/html/' + _PAGE_NAME + _EXTENSION


class PageContentSpider(Spider):
    name = 'page_page'
    handle_httpstatus_list = [301, 302, 204, 206, 404, 500]

    start_urls = [
        'http://www.ygdy8.net/html/gndy/dyzz/index.html'
    ]

    def parse(self, response):
        html_content = response.body
        with open(_PAGE_FILE, 'wb') as f:
            f.write(html_content)
