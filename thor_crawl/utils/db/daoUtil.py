"""
数据库连接工具类
"""
import logging
from datetime import datetime

from thor_crawl.utils.db.mysql.mySQLConfig import MySQLConfig
from thor_crawl.utils.db.mysql.mySQLUtil import MySQLUtil

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
log = logging.getLogger(__name__)


class DaoUtils:
    def __init__(self, *args, **kw):
        # 设置是否打印日志
        self.log = kw['log'] if 'log' in kw else True

        if 'dbType' in kw:
            if 'MySQL' == kw['dbType']:
                self.dao = MySQLUtil(**kw['config'])
            else:
                log.error('dbType error')
        else:
            self.dao = MySQLUtil(**MySQLConfig.localhost())

    # 处理sql日志
    def handle_sql_log(self, sql):
        if self.log:
            log.info(sql)

    # 可定制化获取数据sql
    @staticmethod
    def customizable_get_sql(table, select_list=None, where_dict=None):
        if select_list:
            sql = 'select %s from %s' % (','.join(select_list), table)
        else:
            sql = 'select * from %s' % table

        if where_dict:
            where_list = list()
            for key, value in where_dict.items():
                where_list.append('%s = "%s"' % (key, str(value)))
            sql += ' where %s ' % (' and '.join(where_list))
        return sql

    # 判断数据存不存在, 存在返回true
    def is_exist(self, sql):
        self.handle_sql_log(sql)
        result = self.dao.select_all(sql)
        return True if len(result) > 0 else False

    # 获取一条记录
    def get_one(self, sql):
        self.handle_sql_log(sql)
        return self.dao.select_one(sql)

    # 获取所有记录
    def get_all(self, sql):
        self.handle_sql_log(sql)
        return self.dao.select_all(sql)

    # 添加数据
    def add(self, sql):
        self.handle_sql_log(sql)
        return self.dao.insert(sql)

    # 修改数据
    def modify(self, sql):
        self.handle_sql_log(sql)
        return self.dao.update(sql)

    # 定制化获取一条数据
    def customizable_get_one(self, table, select_list=None, where_dict=None):
        sql = DaoUtils.customizable_get_sql(table, select_list, where_dict)
        self.handle_sql_log(sql)
        return self.dao.select_one(sql)

    # 定制化获取所有数据
    def customizable_get_all(self, table, select_list=None, where_dict=None):
        sql = DaoUtils.customizable_get_sql(table, select_list, where_dict)
        self.handle_sql_log(sql)
        return self.dao.select_all(sql)

    # 插入数据
    def customizable_add(self, table, value_dic, time=False):
        if time:
            gmt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            value_dic['gmt_create'] = gmt
            value_dic['gmt_modify'] = gmt
        sql = 'insert into ' + table + '(' + ','.join(value_dic.keys()) + ') values'
        value_list = list()
        for key, value in value_dic.items():
            value_list.append('\'' + str(value) + '\'')
        sql += '(' + ','.join(value_list) + ')'
        self.handle_sql_log(sql)
        return self.dao.insert(sql)

    # 批量插入数据
    def customizable_add_batch(self, table, data_list, time=True):
        if time:
            gmt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            for data in data_list:
                data['gmt_create'] = gmt
                data['gmt_modify'] = gmt
        sql = 'insert into ' + table + '(' + ','.join(data_list[0].keys()) + ') values'
        value_list = list()
        for data in data_list:
            inner_value_list = list()
            for key, value in data.items():
                if isinstance(value, str):
                    inner_value_list.append('\'' + value + '\'')
                else:
                    inner_value_list.append(str(value))
            value_list.append('(' + ','.join(inner_value_list) + ')')
        sql += ','.join(value_list)
        self.handle_sql_log(sql)
        return self.dao.execute(sql)

    # 批量插入数据(如果存在primary or unique相同的记录，则先删除掉。再插入新记录。)
    def customizable_replace_batch(self, table, data_list, time=True):
        if time:
            gmt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            for data in data_list:
                data['gmt_create'] = gmt
                data['gmt_modify'] = gmt
        sql = 'replace into ' + table + '(' + ','.join(data_list[0].keys()) + ') values'
        value_list = list()
        for data in data_list:
            inner_value_list = list()
            for key, value in data.items():
                if isinstance(value, str):
                    inner_value_list.append('\'' + value + '\'')
                else:
                    inner_value_list.append(str(value))
            value_list.append('(' + ','.join(inner_value_list) + ')')
        sql += ','.join(value_list)
        self.handle_sql_log(sql)
        return self.dao.execute(sql)

    # 更新数据
    def customizable_modify(self, table, db_dict, where_dict, time=True):
        if time:
            db_dict['gmt_modify'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 更新的内容
        value_list = list()
        for key, value in db_dict.items():
            value_list.append('%s = "%s"' % (key, str(value)))

        # 判断内容
        where_list = list()
        where_list.append('1 = 1')
        for key, value in where_dict.items():
            where_list.append('%s = "%s"' % (key, str(value)))

        # 更新的条件
        sql = 'update %s set %s  ' % (table, ','.join(value_list))
        sql += 'where  %s ' % (' and '.join(where_list))
        print(sql)
        return self.dao.execute(sql)


if __name__ == '__main__':
    dao_config = {'dbType': 'MySQL', 'config': MySQLConfig.localhost()}
    dao = DaoUtils(**dao_config)
