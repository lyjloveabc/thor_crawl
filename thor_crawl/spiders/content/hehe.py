#a = 'bid=442OKudequU; douban-fav-remind=1; __yadk_uid=QLsssUg0OHNS05ggccpyGOkrzlR87vRu; ll="118172"; __utmz=30149280.1535852991.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; _vwo_uuid_v2=D999E75B6520205D5493F9E3CBE7EA81A|96a7288963b0c22d4b3a79f944e268ed; _ga=GA1.2.444907684.1535806542; _gid=GA1.2.2119573250.1536416736; push_noty_num=0; push_doumail_num=0; __utmv=30149280.6600; douban-profile-remind=1; ct=y; ps=y; __utmc=30149280; dbcl2="66002721:vcpy2eRrFAY"; ck=znM_; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1536497176%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3Dm6nehSIMaiAfUjiYzC_k2aivJyu-uoAv8zt8ce583ti7I4zYlJv5uCfEEq7NtEWT%26wd%3D%26eqid%3De3939aa4000826b6000000045b93dbdb%22%5D; _pk_ses.100001.8cb4=*; ap_v=0,6.0; __utma=30149280.444907684.1535806542.1536451822.1536497177.5; __utmt=1; _pk_id.100001.8cb4=4b18d8548e2018fd.1535806541.5.1536498740.1536452607.; __utmb=30149280.144.5.1536498741975'
a = """Host: www.douban.com
Connection: keep-alive
Content-Length: 22
Accept: text/plain, */*; q=0.01
Origin: https://www.douban.com
X-Requested-With: XMLHttpRequest
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36
Content-Type: application/x-www-form-urlencoded
Referer: https://www.douban.com/group/topic/90353888/
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9"""

a = a.replace(' ', '')
aaa = a.split('\n')

for x in aaa:
    nn = x.split(':')
    print("'" + nn[0] + "': " + "'" + nn[1] + "',")
