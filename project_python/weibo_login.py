import requests
import re
import base64
import time
import json
from io import BytesIO
from chaojiying import Chaojiying_Client
import rsa
import binascii


class CookieWeibo(object):
    def __init__(self, un, pw):
        self.un = self.enrcryt_un(un)
        self.pw = pw
        self.session = requests.session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
        }

    # 加密user
    def enrcryt_un(self, un):
        return base64.b64encode(un.encode())

    # 加密password
    def enrcrpy_pw(self, pw, result):
        pubkey = rsa.PublicKey(int(result['pubkey'], 16), int('10001', 16))
        pw_str = str(result['servertime']) + '\t' + result['nonce'] + '\n' + pw
        sp = binascii.b2a_hex(rsa.encrypt(pw_str.encode(), pubkey)).decode()
        # print(sp)
        return sp

    # 预登陆
    def prelogin(self):
        url = 'https://login.sina.com.cn/sso/prelogin.php'
        # 构建参数
        params = {
            'entry': 'weibo',
            'callback': 'sinaSSOController.preloginCallBack',
            'su': self.un,
            'rsakt': 'mod',
            'checkpin': '1',
            'client': 'ssologin.js(v1.4.19)',
            '_': round(time.time() * 1000)
        }
        resp = self.session.get(url, headers=self.headers, params=params, verify=False)
        result = re.findall('preloginCallBack\((.*?)\)', resp.text)[0]
        return json.loads(result)

    # 获取验证码
    def get_yan(self, result):
        if result['showpin'] == 1:
            url = 'https://login.sina.com.cn/cgi/pin.php'
            params = {
                'r': '83661264',
                's': '0',
                'p': result['pcid']
            }
            resp = self.session.get(url, headers=self.headers, params=params, verify=False)
            pic = BytesIO(resp.content).getvalue()
            cjy = Chaojiying_Client('m125705171', 'm1257051717', '898279')
            yz = cjy.PostPic(pic, 1005)
            # print(yz)
            return yz['pic_str']
        else:
            return None

    # 模拟登陆
    def login(self, result, captcha):
        url = 'https://login.sina.com.cn/sso/login.php'
        data = {
            'entry': 'weibo',
            'gateway': '1',
            'from': '',
            'savestate': '7',
            'qrcode_flag': 'false',
            'useticket': '1',
            'pagerefer': '',
            'wsseretry': 'servertime_error',
            'vsnf': '1',
            'su': self.un,
            'service': 'miniblog',
            'servertime': result['servertime'],
            'nonce': result['nonce'],
            'pwencode': 'rsa2',
            'rsakv': result['rsakv'],
            'sp': self.enrcrpy_pw(self.pw, result),
            'sr': '1536*864',
            'encoding': 'UTF-8',
            'prelt': '231',
            'url': 'https://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
            'returntype': 'META'
        }
        if captcha:
            data['pcid'] = result['pcid']
            data['door'] = captcha

        resp = self.session.post(url, headers=self.headers, data=data, verify=False)
        # print(resp.text)
        url_2 = re.findall(r'replace\("(.*?)"\);', resp.text)[0]
        # print(url_2)
        return url_2

    # 模拟登陆，第二部
    def url_next(self, url_2):
        resp = self.session.get(url_2, headers=self.headers, verify=False)
        # print(resp.text)
        next_i = re.findall(r'arrURL":\["(.*?)","(.*?)","(.*?)","(.*?)"\]', resp.text)[0]
        # print(next_i)
        for i in next_i:
            i = i.replace('\\', '')
            self.session.get(i, headers=self.headers, verify=False)

    # 启动程序
    def run(self):
        result = self.prelogin()
        url_2 = self.login(result, self.get_yan(result))
        print(url_2)
        self.url_next(url_2)
        self.verify()

    # 验证
    def verify(self):
        resp = self.session.get('https://weibo.com/u/3033624331/home', headers=self.headers)
        print(resp.text)


if __name__ == '__main__':
    a = Cookie_Weibo('user', 'password')
    a.run()
