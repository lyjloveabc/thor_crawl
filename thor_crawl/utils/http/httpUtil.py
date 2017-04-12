import urllib.request


class HttpUtil:
    @staticmethod
    def get_page_content():
        response = urllib.request.urlopen('https://www.baidu.com/')
        return response.read()


if __name__ == '__main__':
    HttpUtil.get_page_content()