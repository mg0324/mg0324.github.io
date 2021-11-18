"""
自动刷新mb的gitee pages服务
https://gitee.com/mgang/plan/pages/rebuild
branch: master
build_directory:
force_https: false
auto_update: false
"""
import requests
# 获取登录后的
#loginParam = {'user_login':'1092017732@qq.com'}
#loginResult = requests.get('https://gitee.com/check_user_login',params=loginParam)
#gsn = loginResult.cookies['gitee-session-n']
#oschina_new_user = loginResult.cookies['oschina_new_user']
#user_locale = loginResult.cookies['user_locale']
#print(loginResult.cookies)
#cookieStr = 'user_locale=zh-CN; oschina_new_user='+oschina_new_user+"; gitee-session-n="+gsn
header = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Length': '89',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': 'oschina_new_user=false; yp_riddler_id=1fc6e7a9-3827-40dc-af09-8360e69ce24d; close_wechat_tour=true; remote_way=ssh; user_locale=zh-CN; tz=Asia%2FShanghai; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22122375%22%2C%22first_id%22%3A%2217abcb4d3ec42e-05a960c7c38f4c-34647600-1764000-17abcb4d3edaa0%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E5%BC%95%E8%8D%90%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22http%3A%2F%2Fgit.oschina.net%2Fmgang%22%2C%22%24latest_utm_source%22%3A%22alading%22%2C%22%24latest_utm_campaign%22%3A%22repo%22%7D%2C%22%24device_id%22%3A%2217abcb4d3ec42e-05a960c7c38f4c-34647600-1764000-17abcb4d3edaa0%22%7D; Hm_lvt_24f17767262929947cc3631f99bfd274=1636860426,1636863976,1637156499,1637158987; gitee_user=true; gitee-session-n=ejdoMUQ2OW1PYm5PNzRMVkYxN0oxSTBDS2lyL01oUkZjTXRpOHRJZjlBMXJwcXJVUXZMYlR3a2RoM29VR3diQkdPdmMzanM1RERIY28vR3l4YjViRExRc21naGFkK2VkQmgvU05jSjlId0tuWFVrTTQyYWxTY0hwbzZTcWg2TmVjSUNmTHdrcEc1aGhTSU1hQmxzTTNpM0Q1eTVCN1VaRldiZkNMeEt2S0ZtbTMvbHFQeXpDcmp2amYyVEJnZ1lGUDhFNnVZRlQreWFwZE5QZlhOVlRNc3lXaDBoaDVBeG4vSFp5T0o2OEhodk5OeFd1WEx4YVVDRmU3dVBoQ3kxSnVhQTlLVXpoZWROUVVJR1RRZ05xbmE5K0ljQnlNdlN5RDQ0ejNERWwvQnErY2pXUTFndUIrSUNwNVMxalJqMWNEYXBEUSt0aUtRaVJST051WEN3czZ1d2RoYUFJZzc1bisrV3B1TlcwWDhjPS0tZVdwTmErOHlXbFZ3N000VnF0ZEIxZz09--beae159dc443c2d6ee85ec0a2f3bae0a991795a9; Hm_lpvt_24f17767262929947cc3631f99bfd274=1637159902',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36',
    'X-CSRF-Token': 'Z05EF2kJRP2xwHMpkNQ+QaQfI+rAmdpG4yiYy7IhnzTiiUaO3TWbngZ6dViaiTG/yOGmrHEt2v1rmcrLVahI5w==',
    'X-Requested-With': 'XMLHttpRequest'
}
data = {'branch': 'master', 'build_directory': '','force_https': 'false','auto_update': 'false'}
r = requests.post("https://gitee.com/mgang/mb/pages/rebuild",data,headers=header)
#print(r.text)
if r.status_code == 200:
    print("刷新成功")
else:
    print("重新部署失败，"+r.text)
