from itl_crawl.utils.db.daoUtil import DaoUtils
from itl_crawl.utils.db.mysql.mySQLConfig import MySQLConfig

DB_ENV = MySQLConfig.localhost()  # 数据库环境
DB_PARAM = {'dbType': 'MySQL', 'config': DB_ENV}  # 数据库参数
DEFAULT_DB_ENV = DaoUtils(**{'dbType': 'MySQL', 'config': DB_ENV})  # 默认使用的数据库
