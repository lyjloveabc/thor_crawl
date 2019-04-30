import pymysql


class MySQLConfig:
    """
    MySQL配置文件
    """

    PORT = 3306
    CHARSET = 'utf8mb4'
    CURSOR_CLASS = pymysql.cursors.DictCursor

    @staticmethod
    def __common_config():
        config = {
            'port': 3306,
            'charset': MySQLConfig.CHARSET,
            'cursorclass': MySQLConfig.CURSOR_CLASS
        }
        return config

    @staticmethod
    def localhost():
        config = MySQLConfig.__common_config()
        config['host'] = '127.0.0.1'
        config['user'] = 'root'
        config['password'] = '123456'
        config['db'] = 'crawler_itl'
        return config

    @staticmethod
    def inner():
        config = MySQLConfig.__common_config()
        config['host'] = '127.0.0.1'
        config['user'] = 'root'
        config['password'] = 'freedom@Lyj0408'
        config['db'] = 'crawler_itl'
        return config
