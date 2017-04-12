"""
歌单类 mapper
"""
from datetime import datetime

from sqlalchemy import Column

from thor_crawl.utils.db.sqlAlchemy.sqlAlchemyUtil import SQL_ALCHEMY_BASE, BaseAttr


class User(SQL_ALCHEMY_BASE, BaseAttr):
    """网易云音乐，用户类"""

    # 表的名字
    __tablename__ = 'm163_user'

    # 表的自有字段
    main_id = Column()
    name = Column()
    track_number_update_time = Column()
    status = Column()
    user_id = Column()
    create_time = Column()
    update_time = Column()
    subscribed_count = Column()
    track_count = Column()
    cloud_track_count = Column()
    cover_img_url = Column()
    cover_img_id = Column()
    description = Column()
    tags = Column()
    play_count = Column()
    track_update_time = Column()
    special_type = Column()
    total_duration = Column()
    tracks = Column()
    subscribed = Column()
    comment_thread_id = Column()
    new_imported = Column()
    ad_type = Column()
    high_quality = Column()
    privacy = Column()
    ordered = Column()
    anonimous = Column()
    share_count = Column()
    cover_img_id_str = Column()
    comment_count = Column()
    creator_id = Column()
    subscriber_id = Column()

    def __init__(self, *args, **kw):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        super().__init__(gmt_create=now, gmt_modify=now, *args, **kw)


class Playlist(SQL_ALCHEMY_BASE, BaseAttr):
    """网易云音乐，歌单类"""

    __tablename__ = 'm163_playlist'

    main_id = Column()
    name = Column(nullable=False)
    track_number_update_time = Column()
    status = Column()
    user_id = Column()
    create_time = Column()
    update_time = Column()
    subscribed_count = Column()
    track_count = Column()
    cloud_track_count = Column()
    cover_img_url = Column()
    cover_img_id = Column()
    description = Column()
    tags = Column()
    play_count = Column()
    track_update_time = Column()
    special_type = Column()
    total_duration = Column()
    tracks = Column()
    subscribed = Column()
    comment_thread_id = Column()
    new_imported = Column()
    ad_type = Column()
    high_quality = Column()
    privacy = Column()
    ordered = Column()
    anonimous = Column()
    share_count = Column()
    cover_img_id_str = Column()
    comment_count = Column()

    def __init__(self, *args, **kw):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        super().__init__(gmt_create=now, gmt_modify=now, *args, **kw)
