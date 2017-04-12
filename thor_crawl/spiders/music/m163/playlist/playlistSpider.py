"""
网易云音乐 热门歌单
http://music.163.com/api/playlist/list?cat=全部&order=hot&offset=0&total=true&limit=2
    code = text_json['code']
    more = text_json['more']
    total = text_json['total']
    play_lists = text_json['playlists']
"""
import json
import logging

import scrapy
from scrapy.spiders import BaseSpider

# 导入SQLAlchemy:
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from thor_crawl.utils.constant.constant import Constant
from thor_crawl.utils.db.mysql.mySQLConfig import MySQLConfig
from thor_crawl.spiders.music.m163.playlist.entity import Playlist


class PlaylistSpider(BaseSpider):
    name = 'music_m163_playlist_hot'
    handle_httpstatus_list = [301, 302, 204, 206, 404, 500]

    def __init__(self):
        logging.info(Constant.SPIDER_INIT)

        # 参数
        self.base_url = 'http://music.163.com/api/playlist/list?cat={cat}&order={order}&offset={offset}&limit={limit}'
        self.cat = '全部'
        self.order = 'hot'
        self.limit = 20

        # 响应数据
        self.source_total = 0
        self.sum_total = 0

        # 持久化
        self.save_threshold = 1000
        self.persistent_data_user = set()
        self.persistent_data_playlist = list()

        # 数据库连接、session
        self.session = PlaylistSpider.get_db_session()

    def __del__(self):
        logging.info(Constant.SPIDER_DEL)

    def start_requests(self):
        start_requests = list()

        offset = 0
        meta = {'offset': offset}
        url = self.base_url.format(cat=self.cat, order=self.order, offset=meta['offset'], limit=self.limit)
        form_request = scrapy.FormRequest(url=url, method='GET', meta=meta)
        start_requests.append(form_request)

        return start_requests

    def closed(self, res):
        logging.info(Constant.SPIDER_CLOSED)
        print('条数校验:', self.source_total, '  <>  ', self.sum_total)

    def parse(self, response):
        text = response.text
        meta = response.meta

        # 解析json数据
        text_json = json.loads(text)

        code = text_json['code']
        more = text_json['more']
        total = text_json['total']
        playlist_group = text_json['playlists']

        # 正常返回数据
        if code == 200:
            self.source_total = total
            self.sum_total += len(playlist_group)

            for playlist_json in playlist_group:
                playlist = self.get_play_list(playlist_json)
                self.persistent_data_playlist.append(playlist)

            # 如果还有数据则继续抓取
            if more:
                meta['offset'] += self.limit
                url = self.base_url.format(cat=self.cat, order=self.order, offset=meta['offset'], limit=self.limit)
                yield scrapy.FormRequest(url=url, method='GET', meta=meta)

    @staticmethod
    def get_play_list(play_list_json):
        param = {
            'main_id': play_list_json['id'],
            'name': play_list_json['name'],
            'track_number_update_time': play_list_json['trackNumberUpdateTime'],
            'status': play_list_json['status'],
            'user_id': play_list_json['userId'],
            'create_time': play_list_json['createTime'],
            'update_time': play_list_json['updateTime'],
            'subscribed_count': play_list_json['subscribedCount'],
            'track_count': play_list_json['trackCount'],
            'cloud_track_count': play_list_json['cloudTrackCount'],
            'cover_img_url': play_list_json['coverImgUrl'],
            'cover_img_id': play_list_json['coverImgId'],
            'description': play_list_json['description'],
            'tags': play_list_json['tags'].join(','),
            'play_count': play_list_json['playCount'],
            'track_update_time': play_list_json['trackUpdateTime'],
            'special_type': play_list_json['specialType'],
            'total_duration': play_list_json['totalDuration'],
            'tracks': play_list_json['tracks'],
            'subscribed': play_list_json['subscribed'],
            'comment_thread_id': play_list_json['commentThreadId'],
            'new_imported': play_list_json['newImported'],
            'ad_type': play_list_json['adType'],
            'high_quality': play_list_json['highQuality'],
            'privacy': play_list_json['privacy'],
            'ordered': play_list_json['ordered'],
            'anonimous': play_list_json['anonimous'],
            'share_count': play_list_json['shareCount'],
            'cover_img_id_str': play_list_json['coverImgId_str'],
            'comment_count': play_list_json['commentCount'],
            'creator_id': play_list_json['creator']['userId'],
            'subscriber_id': play_list_json['subscribers'][0]['userId']
        }

        return Playlist(param)

    @staticmethod
    def get_db_session():
        mysql_config = MySQLConfig.localhost()
        engine = create_engine('mysql+pymysql://{root}:{password}@{localhost}:3306/{db}'
                               .format(root=mysql_config['user'], password=mysql_config['password'], localhost=mysql_config['host'], db=mysql_config['db']))
        # 创建DBSession类型:
        DBSession = sessionmaker(bind=engine)

        # 返回session对象:
        return DBSession()

    def save(self):
        if len(self.persistent_data_playlist) > self.save_threshold:
            try:
                for item in self.persistent_data_playlist:
                    self.session.add(item)
            except OSError:
                self.session = PlaylistSpider.get_db_session()
            finally:
                self.persistent_data_playlist = list()

    def save_final(self):
        if len(self.persistent_data_playlist) > 0:
            try:
                for item in self.persistent_data_playlist:
                    self.session.add(item)
            except OSError:
                self.session = PlaylistSpider.get_db_session()
            finally:
                self.persistent_data_playlist = list()


if __name__ == '__main__':
    pass
    # mysql_config = MySQLConfig.localhost()
    # engine = create_engine('mysql+pymysql://{root}:{password}@{localhost}:3306/{db}'
    #                        .format(root=mysql_config['user'], password=mysql_config['password'],
    #                                localhost=mysql_config['host'], db=mysql_config['db']))
    # # 创建DBSession类型:
    # DBSession = sessionmaker(bind=engine)
    #
    # # 创建session对象:
    # session = DBSession()
    # # 创建新User对象:
    # new_user = Playlist(main_id=4444, name='4444')
    # # 添加到session:
    # session.add(new_user)
    # # 提交即保存到数据库:
    # session.commit()
    # # 关闭session:
    # session.close()
