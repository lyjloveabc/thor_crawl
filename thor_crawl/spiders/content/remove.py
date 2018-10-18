import json

import requests

headers = {
    'Host': 'www.douban.com',
    'Connection': 'keep-alive',
    'Content-Length': '22',
    'Accept': 'text/plain,*/*;q=0.01',
    'Origin': 'https://www.douban.com',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0(Macintosh;IntelMacOSX10_13_6)AppleWebKit/537.36(KHTML,likeGecko)Chrome/69.0.3497.81Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Referer': 'https://www.douban.com/group/topic/90323810/',
    'Accept-Encoding': 'gzip,deflate,br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}
cookies = {
    'bid': '442OKudequU',
    'douban-fav-remind': '1',
    '__yadk_uid': 'QLsssUg0OHNS05ggccpyGOkrzlR87vRu',
    'll': '"118172"',
    '_vwo_uuid_v2': 'D999E75B6520205D5493F9E3CBE7EA81A|96a7288963b0c22d4b3a79f944e268ed',
    '_ga': 'GA1.2.444907684.1535806542',
    'push_noty_num': '0',
    'push_doumail_num': '0',
    '__utmv': '30149280.6600',
    'douban-profile-remind': '1',
    'ct': 'y',
    'ps': 'y',
    '__utmz': '30149280.1536634835.6.3.utmcsr=baidu|utmccn=(organic)|utmcmd=organic',
    '_pk_ref.100001.8cb4': '%5B%22%22%2C%22%22%2C1536717893%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DgLb055XFNzEK3HvCb4tWVIHxgcEMW7tE1Kdh6hSFvZpHVbfjIEzBVo59OM1iQQAH%26wd%3D%26eqid%3D8fe1cdae00017154000000045b972fc3%22%5D',
    '_pk_ses.100001.8cb4': '*',
    'ap_v': '0,6.0',
    '__utma': '30149280.444907684.1535806542.1536634835.1536717895.7',
    '__utmc': '30149280',
    'dbcl2': '"66002721:cLJ0U+SObDQ"',
    'ck': 'KRq5',
    '__utmt': '1',
    '__utmb': '30149280.500.8.1536718676470',
    '_pk_id.100001.8cb4': '4b18d8548e2018fd.1535806541.7.1536719018.1536634843.',
}
payload = {
    'cid': '1193717101',
    'ck': 'KRq5'
}
remove_base_url = 'https://www.douban.com/j/group/topic/90323810/remove_comment'
r = requests.post(remove_base_url, data=payload, headers=headers, cookies=cookies)
print(r)

# Thor (做好事情，波澜不惊)
