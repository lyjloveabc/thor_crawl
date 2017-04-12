import pymysql


class MySQLUtil:
    """
    MySQLUtil工具类
    """

    def __init__(self, *args, **kw):
        # 打开数据库连接
        self.connection = pymysql.connect(*args, **kw)

        # 使用 cursor 方法创建一个游标对象 cursor
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.cursor.close()
        self.connection.close()

    def get_cursor(self):
        return self.cursor

    def select_one(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def select_all(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    # 插入，同时返回最后插入的主键ID
    def insert(self, sql):
        self.cursor.execute(sql)
        last_row_id = int(self.cursor.lastrowid)
        self.connection.commit()
        return last_row_id

    def update(self, sql):
        row_count = self.cursor.execute(sql)
        self.connection.commit()
        return row_count

    def execute(self, sql):
        result = self.cursor.execute(sql)
        self.connection.commit()
        return result
