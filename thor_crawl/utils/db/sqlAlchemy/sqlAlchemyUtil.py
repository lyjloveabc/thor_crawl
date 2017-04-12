"""
orm: sqlAlchemy 工具类
"""
from sqlalchemy import Column
from sqlalchemy import Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类
SQL_ALCHEMY_BASE = declarative_base()


class SqlAlchemyUtil:
    pass


class BaseAttr:
    # 表的公共字段
    id = Column(Integer, primary_key=True)
    gmt_create = Column(DateTime)
    gmt_modify = Column(DateTime)

    def __init__(self, *args, **kw):
        super().__init__()


if __name__ == '__main__':
    pass
