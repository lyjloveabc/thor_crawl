"""
网易云音乐 热门歌单
http://music.163.com/api/playlist/list?cat=全部&order=hot&offset=0&total=true&limit=2
    code = text_json['code']
    more = text_json['more']
    total = text_json['total']
    play_lists = text_json['playlists']
"""
import json

import scrapy
from scrapy.spiders import BaseSpider

# 导入SQLAlchemy:
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from thor_crawl.utils.db.mysql.mySQLConfig import MySQLConfig
from thor_crawl.spiders.music.music163.playlist.playlist import Playlist


class PlaylistSpider(BaseSpider):
    name = 'music_music163_playlist_hot'
    handle_httpstatus_list = [301, 302, 204, 206, 404, 500]

    def __init__(self):
        print('---spider __init__!')
        self.base_url = 'http://music.163.com/api/playlist/list?cat={cat}&order={order}&offset={offset}&limit={limit}'
        self.cat = '全部'
        self.order = 'hot'
        self.limit = 20
        self.source_total = 0
        self.sum_total = 0

    def __del__(self):
        print('---spider __del__!')

    def start_requests(self):
        start_requests = list()

        offset = 0
        meta = {'offset': offset}
        url = self.base_url.format(cat=self.cat, order=self.order, offset=meta['offset'], limit=self.limit)
        form_request = scrapy.FormRequest(url=url, method='GET', meta=meta)
        start_requests.append(form_request)

        return start_requests

    def closed(self, res):
        print('---spider closed!')
        print(self.source_total, '  <>  ', self.sum_total)

    def parse(self, response):
        text = response.text
        meta = response.meta

        # 解析json数据
        text_json = json.loads(text)

        code = text_json['code']
        more = text_json['more']
        total = text_json['total']
        play_lists = text_json['playlists']

        # 正常返回数据
        if code == 200:
            self.source_total = total
            self.sum_total += len(play_lists)

            for play_list_json in play_lists:
                play_list = self.get_play_list(play_list_json)

            # 如果还有数据则继续抓取
            if more:
                meta['offset'] += self.limit
                url = self.base_url.format(cat=self.cat, order=self.order, offset=meta['offset'], limit=self.limit)
                yield scrapy.FormRequest(url=url, method='GET', meta=meta)

    def get_play_list(self, play_list_json):
        main_id = play_list_json['id']
        name = play_list_json['name']
        track_number_update_time = play_list_json['trackNumberUpdateTime']
        status = play_list_json['status']
        user_id = play_list_json['userId']
        create_time = play_list_json['createTime']
        update_time = play_list_json['updateTime']
        subscribed_count = play_list_json['subscribedCount']

        track_count = play_list_json['trackCount']
        cloud_track_count = play_list_json['cloudTrackCount']
        cover_img_url = play_list_json['coverImgUrl']
        cover_img_id = play_list_json['coverImgId']
        description = play_list_json['description']
        tags = play_list_json['tags'].join(',')
        cover_img_id = play_list_json['coverImgId']
        cover_img_id = play_list_json['coverImgId']

        Playlist(main_id=main_id, name=name, track_number_update_time=track_number_update_time, status=status,
                 user_id=user_id, create_time=create_time, update_time=update_time, subscribed_count=subscribed_count,
                 track_count=track_count, cloud_track_count=cloud_track_count, cover_img_url=cover_img_url,
                 cover_img_id=cover_img_id, description=description)
        return 1


if __name__ == '__main__':
    mysql_config = MySQLConfig.localhost()
    engine = create_engine('mysql+pymysql://{root}:{password}@{localhost}:3306/{db}'
                           .format(root=mysql_config['user'], password=mysql_config['password'],
                                   localhost=mysql_config['host'], db=mysql_config['db']))
    # 创建DBSession类型:
    DBSession = sessionmaker(bind=engine)

    # 创建session对象:
    session = DBSession()
    # 创建新User对象:
    new_user = Playlist(main_id=4444, name='4444')
    # 添加到session:
    session.add(new_user)
    # 提交即保存到数据库:
    session.commit()
    # 关闭session:
    session.close()
