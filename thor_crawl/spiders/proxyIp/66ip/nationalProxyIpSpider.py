"""
网易云音乐 多种歌单
http://music.163.com/api/playlist/list?cat=全部&order=hot&offset=0&total=true&limit=2

http://music.163.com/api/playlist/list?cat=全部&order=hot&limit=2&offset=0
    code = text_json['code']
    more = text_json['more']
    total = text_json['total']
    play_lists = text_json['playlists']
"""
import json
import logging

import re
import scrapy
from scrapy.spiders import Spider

from thor_crawl.utils.constant.constant import Constant

from thor_crawl.utils.commonUtil import CommonUtil
from thor_crawl.utils.db.daoUtil import DaoUtils


class NationalProxyIpSpider(Spider):
    name = 'proxyIp_66ip_nationalProxyIp'
    handle_httpstatus_list = [301, 302, 204, 206, 404, 500]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logging.info(Constant.SPIDER_INIT)

        # ============ 工具 ============
        self.dao = DaoUtils()
        self.common_util = CommonUtil()

        # 参数
        self.base_url = 'http://www.66ip.cn/1.html'
        self.limit = 20
        self.cats = ['全部', '华语', '欧美', '日语', '韩语', '粤语', '小语种',
                     '流行', '摇滚', '民谣', '电子', '舞曲', '说唱', '轻音乐', '爵士', '乡村', 'R&B/Soul', '古典', '民族', '英伦', '金属',
                     '朋克', '蓝调', '雷鬼', '世界音乐', '拉丁', '另类/独立', 'New Age', '古风',
                     '后摇', 'Bossa Nova',
                     '清晨', '夜晚', '学习', '工作', '午休', '下午茶', '地铁', '驾车', '运动', '旅行', '散步', '酒吧',
                     '怀旧', '清新', '浪漫', '性感', '伤感', '治愈', '放松', '孤独', '感动', '兴奋', '快乐', '安静', '思念',
                     '影视原声', 'ACG', '校园', '游戏', '70后', '80后', '90后', '网络歌曲', 'KTV', '经典', '翻唱', '吉他', '钢琴', '器乐', '儿童', '榜单', '00后']
        self.orders = ['hot', 'new']

        # 响应数据
        self.source_total = dict()  # 数据源数据
        self.sum_total = 0  # 抓取数据

        # 持久化
        self.main_table = 'm163_playlist'
        self.user_table = 'm163_user'
        self.save_threshold = 100
        self.persistent_data_user = list()
        self.persistent_data_playlist = list()

    def __del__(self):
        logging.info(Constant.SPIDER_DEL)
        self.save_final()

    def start_requests(self):
        start_requests = list()

        url = 'http://www.66ip.cn/1.html'
        meta = {
            'page_num': 1
        }

        form_request = scrapy.FormRequest(url=url, method='GET', meta=meta)
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

        # 解析json数据
        text_json = json.loads(text)

        code = text_json['code']
        more = text_json['more']
        total = text_json['total']
        playlist_group = text_json['playlists']

        # 正常返回数据
        if code == 200:
            url_group = re.search(r'(.+)&offset=(\d+)', url)
            front = url_group.group(1)

            self.source_total[front] = total
            self.sum_total += len(playlist_group)

            for playlist_json in playlist_group:
                playlist = self.get_play_list(playlist_json)
                user = self.get_user(playlist_json['creator'])

                playlist['url_cat'] = meta['url_cat']
                playlist['url_order'] = meta['url_order']

                self.persistent_data_playlist.append(playlist)
                self.persistent_data_user.append(user)

                if len(playlist_json['subscribers']) > 0:
                    subscriber = self.get_user(playlist_json['subscribers'][0])
                    self.persistent_data_user.append(subscriber)

            # 如果还有数据则继续抓取
            if more:
                meta['offset'] += self.limit
                next_url = front + '&offset=' + str(meta['offset'])
                yield scrapy.FormRequest(url=next_url, method='GET', meta=meta)

        self.save()

    @staticmethod
    def get_play_list(playlist_json):
        param = {
            'main_id': playlist_json['id'],
            'name': playlist_json['name'],
            'track_number_update_time': playlist_json['trackNumberUpdateTime'],
            'status': playlist_json['status'],
            'user_id': playlist_json['userId'],
            'create_time': playlist_json['createTime'],
            'update_time': playlist_json['updateTime'],
            'subscribed_count': playlist_json['subscribedCount'],
            'track_count': playlist_json['trackCount'],
            'cloud_track_count': playlist_json['cloudTrackCount'],
            'cover_img_url': playlist_json['coverImgUrl'],
            'cover_img_id': playlist_json['coverImgId'],
            'description': playlist_json['description'],
            'tags': Constant.DEFAULT_SEP.join(playlist_json['tags']),
            'play_count': playlist_json['playCount'],
            'track_update_time': playlist_json['trackUpdateTime'],
            'special_type': playlist_json['specialType'],
            'total_duration': playlist_json['totalDuration'],
            'tracks': playlist_json['tracks'],
            'subscribed': playlist_json['subscribed'],
            'comment_thread_id': playlist_json['commentThreadId'],
            'new_imported': playlist_json['newImported'],
            'ad_type': playlist_json['adType'],
            'high_quality': playlist_json['highQuality'],
            'privacy': playlist_json['privacy'],
            'ordered': playlist_json['ordered'],
            'anonimous': playlist_json['anonimous'],
            'share_count': playlist_json['shareCount'],
            'cover_img_id__str': playlist_json['coverImgId_str'] if 'coverImgId_str' in playlist_json else Constant.STR_EMPTY,
            'comment_count': playlist_json['commentCount'],
            'creator_id': playlist_json['creator']['userId'],
            'subscriber_id': playlist_json['subscribers'][0]['userId'] if len(playlist_json['subscribers']) > 0 else 0
        }

        for key, value in param.items():
            if param[key] is None:
                param[key] = ''
            value_str = str(param[key])
            if '\'' in value_str:
                param[key] = value_str.replace('\'', '"')

        return param

    @staticmethod
    def get_user(user_json):
        param = {
            'default_avatar': user_json['defaultAvatar'],
            'province': user_json['province'],
            'auth_status': user_json['authStatus'],
            'followed': user_json['followed'],
            'avatar_url': user_json['avatarUrl'],
            'account_status': user_json['accountStatus'],
            'gender': user_json['gender'],
            'city': user_json['city'],
            'birthday': user_json['birthday'],
            'user_id': user_json['userId'],
            'user_type': user_json['userType'],
            'nickname': user_json['nickname'],
            'signature': user_json['signature'],
            'description': user_json['description'],
            'detail_description': user_json['detailDescription'],
            'avatar_img_id': user_json['avatarImgId'],
            'background_img_id': user_json['backgroundImgId'],
            'background_url': user_json['backgroundUrl'],
            'authority': user_json['authority'],
            'mutual': user_json['mutual'],
            'expert_tags': Constant.STR_EMPTY if user_json['expertTags'] is None else Constant.DEFAULT_SEP.join(user_json['expertTags']),
            'dj_status': user_json['djStatus'],
            'vip_type': user_json['vipType'],
            'remark_name': user_json['remarkName'],
            'avatar_img_id_str': user_json['avatarImgIdStr'],
            'background_img_id_str': user_json['backgroundImgIdStr'],
            'avatar_img_id__str': user_json['avatarImgId_str'] if 'avatarImgId_str' in user_json else Constant.STR_EMPTY
        }

        for key, value in param.items():
            if param[key] is None:
                param[key] = ''
            value_str = str(param[key])
            if '\'' in value_str:
                param[key] = value_str.replace('\'', '"')

        return param

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
    logging.info(NationalProxyIpSpider)
