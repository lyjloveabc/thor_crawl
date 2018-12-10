self.cookies = {
    'u': '621544438231589',
    's': 'eq13zbsfyd',
    'device_id': '15e29e08eb8eabfad484e4f725fba482',
    'snbim_minify': 'true',
}
self.headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:63.0) Gecko/20100101 Firefox/63.0',
    'Cookie': '_ga=GA1.2.622531642.1537177620; device_id=15e29e08eb8eabfad484e4f725fba482; s=eq13zbsfyd; bid=193a704f707fd9e5d38e9258755772d3_jn00hppu; aliyungf_tc=AQAAANX82DG0hQMAet/nc6o08xOdn7Z6; _gid=GA1.2.1434884156.1544420139; snbim_minify=true; xq_a_token=6125633fe86dec75d9edcd37ac089d8aed148b9e; xq_a_token.sig=CKaeIxP0OqcHQf2b4XOfUg-gXv0; xq_r_token=335505f8d6608a9d9fa932c981d547ad9336e2b5; xq_r_token.sig=i9gZwKtoEEpsL9Ck0G7yUGU42LY; u=621544438231589; Hm_lvt_1db88642e346389874251b5a1eded6e3=1544161803,1544420139,1544438050,1544451680; __utma=1.622531642.1537177620.1544082461.1544451680.61; __utmc=1; __utmz=1.1544451680.61.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmb=1.1.10.1544451680; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1544452116',
}


response = requests.get(self.page_list_url.format(user_id=self.user_id, page_num=1), cookies=self.cookies, headers=self.headers)