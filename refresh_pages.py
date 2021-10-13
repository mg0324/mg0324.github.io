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
    'Cookie': 'user_locale=zh-CN; oschina_new_user=false; gitee-session-n=V0MvWGpjNTNHby9ZQnoyVmVrYkliZjNycWFROThqVHluSW5Jc0prQ1lEeXE0cWw3RDNIRC84WVRPYVRPNWR5Um1MUWZuOWdKYStHODZQTStXeDhRZHdrbTlrUGFXd3lQMGF5THh3YUJGeUNidzFMNFVoMUZFd0NNeHFXclA2NEI2UnFZaTVJTDg3bWhiZXVKSklpb05tTjZIdU55UWlWTm5TNjFTWWhrRE5MZ1pmbWV1OTBUVXBxUUNOSTl4b2kxK0d5elV2Nk4yMnR4N1V2am9oTTdBZkdEZGVIUWsycDNnc2dHeTVweFVrL1NZa3g1RytEQ21nMk5rNCtyUUVIWFdoQktlS0ZScjhCaDlJSFR5Ujk4cFh1SVFacEEwUlpUQSsvaUpMOGE4WVlQeDhOWTFSMHNlbGVYSUtPeEZkYXRwSzBqMWVNaTZDUnlheVAwOFBoMFRFOGErSlNVUGczQTdiWHNFTC9ERm9JPS0tRXdaUE5LNnk2UWVsNjREM2JsL2JQdz09--04bbd7e485ad58a68fe05a76b05fab46d160cbd0',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36',
    'X-CSRF-Token': 'xsiO1ixyqNQb6Z/Q637HwRAKT7xrkHIsD40vODmaNN0=',
    'X-Requested-With': 'XMLHttpRequest'
}
data = {'branch': 'master', 'build_directory': '','force_https': 'false','auto_update': 'false'}
r = requests.post("https://gitee.com/mgang/mb/pages/rebuild",data,headers=header)
#print(r.text)
if r.status_code == 200:
    print("refresh success!!!")
