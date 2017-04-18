"""
网易云音乐 歌单包含的歌曲
http://music.163.com/api/playlist/detail?id=695550541

select * from m163_playlist where url_cat = '全部';
"""
import json
import logging
import time

import scrapy
from pymysql import OperationalError
from scrapy.spiders import Spider

from thor_crawl.spiders.music.m163.m163Constant import M163Constant
from thor_crawl.utils.constant.constant import Constant

from thor_crawl.utils.commonUtil import CommonUtil
from thor_crawl.utils.db.daoUtil import DaoUtils
from thor_crawl.utils.system.systemUtil import SystemUtil


class ArtistSongSpider(Spider):
    name = 'music_m163_song_artistSong'
    handle_httpstatus_list = [301, 302, 204, 206, 404, 500]

    _PAGE_FILE = 'spiders/music/m163/song/file/'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logging.info(Constant.SPIDER_INIT)

        # ============ 工具 ============
        self.dao = DaoUtils()
        self.common_util = CommonUtil()

        self.base_url = 'http://music.163.com/api/playlist/detail?id={id}'

        # ============ 数据库数据 ============
        self.playlist_id_group = set()
        with open(ArtistSongSpider._PAGE_FILE + 'hot_folt.txt', 'r') as f:
            for line in f.readlines():
                self.playlist_id_group.add(line[:-1])

        # ============ 持久化 ============
        self.save_threshold = 100

        self.m163_song_table = 'm163_song'
        self.m163_music_level_table = 'm163_music_level'
        self.m163_playlist_x_song_table = 'm163_playlist_x_song'

        self.persistent_data_song = list()
        self.persistent_data_music_level = list()
        self.persistent_data_playlist_x_song = list()

        self.flag = 0

    def __del__(self):
        logging.info(Constant.SPIDER_DEL)
        self.save_final()

    def start_requests(self):
        start_requests = list()

        for playlist_id in self.playlist_id_group:
            form_request = scrapy.FormRequest(url=self.base_url.format(id=playlist_id), method='GET',
                                              headers=M163Constant.HEADERS, cookies=M163Constant.COOKIES)
            start_requests.append(form_request)

        return start_requests

    def closed(self, res):
        logging.info(Constant.SPIDER_CLOSED)
        self.save_final()

    def parse(self, response):
        text = response.text

        # 解析json数据
        text_json = json.loads(text)

        result = text_json['result']
        code = text_json['code']

        self.flag += 1

        # 正常返回数据
        if code == 200:
            for track_json in result['tracks']:
                music_levels = self.get_music_level(track_json)
                track = self.get_play_list_track(track_json)
                music_level_group = self.get_play_list_music_level_group(music_levels, track['m163_id'])

                self.persistent_data_song.append(track)
                self.persistent_data_music_level += music_level_group
                self.persistent_data_playlist_x_song.append({'m163_playlist_id': result['id'], 'm163_song_id': track['m163_id']})

        if self.flag == 50:
            time.sleep(10)

        self.save()

    @staticmethod
    def get_play_list_track(json_str):
        artist_ids = []

        artists = json_str['artists']
        for artist in artists:
            artist_ids.append(str(artist['id']))

        param = {
            'm163_id': json_str['id'],
            'name': json_str['name'],
            'position': json_str['position'],
            'alias': ','.join(json_str['alias']) if len(json_str['alias']) > 0 else '',
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
            'mv_id': json_str['mvid'],
            'mp3_url': json_str['mp3Url'],
            'rtype': json_str['rtype'],
            'r_url': json_str['rurl'],
            'artist_ids': str(','.join(artist_ids)),
            'first_artist_id': artists[0]['id'],
            'first_artist_name': artists[0]['name'],
            'first_artist_pic_url': artists[0]['picUrl'],
            'album_id': json_str['album']['id'],
            'b_music_id': json_str['bMusic']['id'] if 'bMusic' in json_str and json_str['bMusic'] is not None else -1,
            'h_music_id': json_str['hMusic']['id'] if 'hMusic' in json_str and json_str['hMusic'] is not None else -1,
            'm_music_id': json_str['mMusic']['id'] if 'mMusic' in json_str and json_str['mMusic'] is not None else -1,
            'l_music_id': json_str['lMusic']['id'] if 'lMusic' in json_str and json_str['lMusic'] is not None else -1
        }

        return SystemUtil.dict_value_handle(param)

    @staticmethod
    def get_play_list_music_level_group(music_levels, track_id):
        music_level_group = list()

        for music_level in music_levels:
            param = {
                'music_level_id': music_level['id'],
                'name': music_level['name'],
                'size': music_level['size'],
                'extension': music_level['extension'],
                'sr': music_level['sr'],
                'dfs_id': music_level['dfsId'],
                'bitrate': music_level['bitrate'],
                'play_time': music_level['playTime'],
                'volume_delta': music_level['volumeDelta'],
                'music_level': music_level['music_level'],
                'm163_song_id': track_id
            }
            music_level_group.append(SystemUtil.dict_value_handle(param))

        return music_level_group

    def save(self):
        self.save_detail(self.m163_song_table, self.persistent_data_song, self.save_threshold)
        self.save_detail(self.m163_music_level_table, self.persistent_data_music_level, self.save_threshold)
        self.save_detail(self.m163_playlist_x_song_table, self.persistent_data_playlist_x_song, self.save_threshold)

        self.persistent_data_song = list()
        self.persistent_data_music_level = list()
        self.persistent_data_playlist_x_song = list()

    def save_final(self):
        self.save_final_detail(self.m163_song_table, self.persistent_data_song)
        self.save_final_detail(self.m163_music_level_table, self.persistent_data_music_level)
        self.save_final_detail(self.m163_playlist_x_song_table, self.persistent_data_playlist_x_song)

    def save_detail(self, table, persistent_data, save_threshold):
        if len(persistent_data) > save_threshold:
            try:
                self.dao.customizable_replace_batch(table, persistent_data)
            except OperationalError as e:
                self.dao = DaoUtils()
                self.dao.customizable_replace_batch(table, persistent_data)
                logging.error('save except:', e)
            finally:
                pass

    def save_final_detail(self, table, persistent_data):
        if len(persistent_data) > 0:
            try:
                self.dao.customizable_replace_batch(table, persistent_data)
            except OperationalError as e:
                self.dao = DaoUtils()
                self.dao.customizable_replace_batch(table, persistent_data)
                logging.error('save_final except:', e)
            finally:
                pass

    @staticmethod
    def get_music_level(track_json):
        music_levels = list()

        if 'hMusic' in track_json and track_json['hMusic'] is not None:
            track_json['hMusic']['music_level'] = 'hMusic'
            music_levels.append(track_json['hMusic'])
        if 'mMusic' in track_json and track_json['mMusic'] is not None:
            track_json['mMusic']['music_level'] = 'mMusic'
            music_levels.append(track_json['mMusic'])
        if 'lMusic' in track_json and track_json['lMusic'] is not None:
            track_json['lMusic']['music_level'] = 'lMusic'
            music_levels.append(track_json['lMusic'])
        if 'bMusic' in track_json and track_json['bMusic'] is not None:
            track_json['bMusic']['music_level'] = 'bMusic'
            music_levels.append(track_json['bMusic'])

        return music_levels


if __name__ == '__main__':
    logging.info(ArtistSongSpider)
