"""
比对(不比对逻辑上已经删除了的, 每次从数据库取1000, 处理完之后清空缓存, 再取1000), 有效的设置为Y, 失效的设置为N
"""

import logging

from thor_crawl.utils.db.daoUtil import DaoUtils
from thor_crawl.utils.http.proxyIpUtil import ProxyIpUtil

logger = logging.getLogger(__name__)


class VerifyProxyIp(object):
    # 数据库表
    __DB_TABLE_MAIN = 'proxy_ip'

    def __init__(self):
        self.dao = DaoUtils()

    def handle(self):
        proxy_ip_group = self.dao.get_all('select id, ip, port, ip_type from ' + VerifyProxyIp.__DB_TABLE_MAIN)
        for proxy_ip_row in proxy_ip_group:
            ip_type = proxy_ip_row['ip_type'].lower()
            proxy_ip = ip_type + '://' + proxy_ip_row['ip'] + ':' + proxy_ip_row['port']
            if ProxyIpUtil.is_effective(ip_type, proxy_ip):
                self.dao.modify('update ' + VerifyProxyIp.__DB_TABLE_MAIN + ' set status = 1 where id = ' + proxy_ip_row['id'])
                print(1111)
            else:
                self.dao.modify('update ' + VerifyProxyIp.__DB_TABLE_MAIN + ' set status = 0 where id = ' + proxy_ip_row['id'])
                print(2222)


if __name__ == '__main__':
    while True:
        print(VerifyProxyIp().handle())
