"""
歌单类 mapper
"""
from datetime import datetime

from sqlalchemy import Column

from thor_crawl.utils.db.sqlAlchemy.sqlAlchemyUtil import SQL_ALCHEMY_BASE, BaseAttr


class Playlist(SQL_ALCHEMY_BASE, BaseAttr):
    """网易云音乐，歌单类"""

    # 表的名字
    __tablename__ = 'playlist'

    # 表的自有字段
    main_id = Column()
    name = Column()
    track_number_update_time = Column()
    status = Column()
    user_id = Column()
    create_time = Column()
    update_time = Column()
    subscribed_count = Column()

    def __init__(self, *args, **kw):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        super().__init__(gmt_create=now, gmt_modify=now, *args, **kw)
