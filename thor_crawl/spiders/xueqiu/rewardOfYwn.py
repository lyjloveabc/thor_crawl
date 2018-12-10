"""
统计雪球大V元卫南收到的打赏金额
元卫南的原创专栏地址：https://xueqiu.com/2227798650/column
元卫南的原创专栏分页列表数据第一页的API：https://xueqiu.com/statuses/original/timeline.json?user_id=2227798650&page=1
元卫南的原创专栏某一篇文章的打赏数据的API：https://xueqiu.com/statuses/reward/list_by_user.json?status_id=118077741&page=1&size=14

列表的每一项有一个超链接，通过这个超链接可以组装这一项对应的详情的打赏API
"""

import json

import requests


class RewardOfYwn:
    def __init__(self):
        self.domain = 'https://xueqiu.com'  # 雪球的域名
        self.page_list_api = 'https://xueqiu.com/statuses/original/timeline.json?user_id={user_id}&page={page_num}'  # 雪球某个人的帖子分页数据API
        self.reward_api = 'https://xueqiu.com/statuses/reward/list_by_user.json?status_id={status_id}&page=1&size=20'  # 某个帖子的打赏数据API

        self.user_id = '2227798650'  # 元卫南的用户ID

        self.headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:63.0) Gecko/20100101 Firefox/63.0',
            'Cookie': '_ga=GA1.2.622531642.1537177620; device_id=15e29e08eb8eabfad484e4f725fba482; s=eq13zbsfyd; '
                      'bid=193a704f707fd9e5d38e9258755772d3_jn00hppu; aliyungf_tc=AQAAANX82DG0hQMAet/nc6o08xOdn7Z6; '
                      '_gid=GA1.2.1434884156.1544420139; snbim_minify=true; xq_a_token=6125633fe86dec75d9edcd37ac089d8aed148b9e; '
                      'xq_a_token.sig=CKaeIxP0OqcHQf2b4XOfUg-gXv0; xq_r_token=335505f8d6608a9d9fa932c981d547ad9336e2b5; '
                      'xq_r_token.sig=i9gZwKtoEEpsL9Ck0G7yUGU42LY; u=621544438231589; '
                      'Hm_lvt_1db88642e346389874251b5a1eded6e3=1544161803,1544420139,1544438050,1544451680; '
                      '__utma=1.622531642.1537177620.1544082461.1544451680.61; __utmc=1; '
                      '__utmz=1.1544451680.61.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; '
                      '__utmb=1.1.10.1544451680; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1544452116',
        }  # 构造请求头，主要是user-agent、Cookie

        self.sum_after_deduct_fee = 0  # 雪球扣除1%的服务费后元卫南拿到的打赏总额
        self.sum_from_other_person = 0  # 所有人给元卫南打赏了多少钱，即在元卫南拿到的钱的基础上加上1%的服务费

    def crawl(self):
        """
        主要的爬取逻辑
        :return: 收到的打赏总额sum_after_deduct_fee，球友打赏的总额sum_from_other_person，
                 两者相差1%的服务费，记得总额都要除以100，因为雪球金额的表示法是乘以100的，比如98.12雪球表示成了9812
        """
        first_page_response = requests.get(self.page_list_api.format(user_id=self.user_id, page_num=1), headers=self.headers)  # 先请求第一页的数据，获取总共有多少页等相关信息

        first_page_json_data = json.loads(first_page_response.text)  # 解析第一页的数据

        max_page = first_page_json_data['maxPage']  # 原创文章最多有几个分页列表

        total_reward = self.sum_reward_in_page(first_page_json_data)  # 第一页的打赏总额

        for page_num in range(2, max_page + 1):
            response = requests.get(self.page_list_api.format(user_id=self.user_id, page_num=page_num), headers=self.headers)  # 分页请求
            json_data = json.loads(response.text)  # 解析数据

            total_reward += self.sum_reward_in_page(json_data)

        return {'sum_after_deduct_fee': total_reward / 100, 'sum_from_other_person': total_reward / 0.99 / 100}

    def sum_reward_in_page(self, json_data):
        result = 0

        if json_data is not None and 'list' in json_data and len(json_data['list']) > 0:
            for row in json_data['list']:
                reward_response = requests.get(self.reward_api.format(status_id=row['id']), headers=self.headers)  # 获取打赏数据
                reward_data = json.loads(reward_response.text)  # 解析打赏数据

                result += int(reward_data['reward_amount'])  # 累加打赏的钱

        return result


if __name__ == '__main__':
    obj = RewardOfYwn()
    print(obj.crawl())
