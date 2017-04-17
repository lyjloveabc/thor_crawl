"""
网易云音乐 歌单包含的歌曲
http://music.163.com/api/playlist/detail?id=695550541

select * from m163_playlist where url_cat = '全部';
"""
import json
import logging

import scrapy
from scrapy.spiders import Spider

from thor_crawl.spiders.music.m163.m163Constant import M163Constant
from thor_crawl.utils.constant.constant import Constant

from thor_crawl.utils.commonUtil import CommonUtil
from thor_crawl.utils.db.daoUtil import DaoUtils


class AlbumSpider(Spider):
    name = 'music_m163_album_album'
    handle_httpstatus_list = [301, 302, 204, 206, 404, 500]

    _PAGE_FILE = 'spiders/music/m163/song/file/'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        logging.info(Constant.SPIDER_INIT)

        # ============ 工具 ============
        self.dao = DaoUtils()
        self.common_util = CommonUtil()

        self.base_url = 'http://music.163.com/api/album/{album_id}'

        # ============ 数据库数据 ============
        self.playlist_id_group = set()
        with open(AlbumSpider._PAGE_FILE + 'playlist_hot_main_id.txt', 'r') as f:
            for line in f.readlines():
                self.playlist_id_group.add(line[:-1])

        # 持久化
        self.main_table = 'm163_playlist'
        self.user_table = 'm163_user'
        self.save_threshold = 100
        self.persistent_data_user = list()
        self.persistent_data_playlist = list()

        self.playlist_id_group = [35093341]

    def __del__(self):
        logging.info(Constant.SPIDER_DEL)
        self.save_final()

    def start_requests(self):
        start_requests = list()

        for playlist_id in self.playlist_id_group:
            form_request = scrapy.FormRequest(url=self.base_url.format(album_id=playlist_id), method='GET',
                                              headers=M163Constant.HEADERS, cookies=M163Constant.COOKIES)
            start_requests.append(form_request)

        return start_requests

    def closed(self, res):
        logging.info(Constant.SPIDER_CLOSED)
        sum_source_total = 0
        for value in self.source_total.values():
            sum_source_total += value
        print('条数校验:', sum_source_total, '  <>  ', self.sum_total)
        self.save_final()

    def parse(self, response):
        text = response.text
        meta = response.meta
        url = response.url

        print(response.body)
        print(text)
        # 解析json数据
        text_json = json.loads(text)

        self.save()

    @staticmethod
    def get_play_list_track(json_str):
        artist_ids = []

        artists = json_str['artists']
        for artist in artists:
            artist_ids.append(artist['id'])

        param = {
            'm163_id': json_str['id'],
            'name': json_str['name'],
            'position': json_str['position'],
            'alias': json_str['alias'],
            'status': json_str['status'],
            'fee': json_str['fee'],
            'copyright_id': json_str['copyrightId'],
            'disc': json_str['disc'],
            'no': json_str['no'],
            'starred': json_str['starred'],
            'popularity': json_str['popularity'],
            'score': json_str['score'],
            'starred_num': json_str['starredNum'],
            'duration': json_str['duration'],
            'played_num': json_str['playedNum'],
            'day_plays': json_str['dayPlays'],
            'hear_time': json_str['hearTime'],
            'ring_tone': json_str['ringtone'],
            'crbt': json_str['crbt'],
            'audition': json_str['audition'],
            'copy_from': json_str['copyFrom'],
            'comment_thread_id': json_str['commentThreadId'],
            'rt_url': json_str['rtUrl'],
            'f_type': json_str['ftype'],
            'rt_urls': json_str['rtUrls'],
            'copyright': json_str['copyright'],
            'mv_id': json_str['mvid'],
            'mp3_url': json_str['mp3_url'],
            'rtype': json_str['rtype'],
            'r_url': json_str['rurl'],
            'artist_ids': ','.join(artist_ids),
            'album_id': json_str['album']['id'],
            'b_music_id': json_str['bMusic']['id'],
            'h_music_id': json_str['hMusic']['id'],
            'm_music_id': json_str['mMusic']['id'],
            'l_music_id': json_str['lMusic']['id']
        }

        for key, value in param.items():
            value_str = str(param[key])
            if '\'' in value_str:
                param[key] = value_str.replace('\'', '"')

        return param

    @staticmethod
    def get_play_list_track_artist_group(items):
        artist_group = list()

        for item in items:
            param = {
                'name': item['name'],
                'm163_id': item['id'],
                'pic_url': item['picUrl']
            }

            artist_group.append(param)

        return artist_group

    def save(self):
        if len(self.persistent_data_playlist) > self.save_threshold:
            try:
                self.dao.customizable_replace_batch(self.main_table, self.persistent_data_playlist)
            except AttributeError as e:
                self.dao = DaoUtils()
                self.dao.customizable_replace_batch(self.main_table, self.persistent_data_playlist)
                logging.error('save except:', e)
            finally:
                self.persistent_data_playlist = list()
        if len(self.persistent_data_user) > self.save_threshold:
            try:
                self.dao.customizable_replace_batch(self.user_table, self.persistent_data_user)
            except AttributeError as e:
                self.dao = DaoUtils()
                self.dao.customizable_replace_batch(self.user_table, self.persistent_data_user)
                logging.error('save except:', e)
            finally:
                self.persistent_data_user = list()

    def save_final(self):
        if len(self.persistent_data_playlist) > 0:
            try:
                self.dao.customizable_replace_batch(self.main_table, self.persistent_data_playlist)
            except AttributeError as e:
                self.dao = DaoUtils()
                self.dao.customizable_replace_batch(self.main_table, self.persistent_data_playlist)
                logging.error('save_final except:', e)
            finally:
                self.persistent_data_playlist = list()
        if len(self.persistent_data_user) > 0:
            try:
                self.dao.customizable_replace_batch(self.user_table, self.persistent_data_user)
            except AttributeError as e:
                self.dao = DaoUtils()
                self.dao.customizable_replace_batch(self.user_table, self.persistent_data_user)
                logging.error('save_final except:', e)
            finally:
                self.persistent_data_user = list()


if __name__ == '__main__':
    logging.info(AlbumSpider)
