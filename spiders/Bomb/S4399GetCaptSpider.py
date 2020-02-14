#!/usr/bin/python3
# coding:utf-8
import requests


class S4399GetCaptSpider:
    def __init__(self):
        self.url_captcha = 'http://ptlogin.4399.com/ptlogin/captcha.do'

        self.Sess = requests.Session()

    def get_captcha(self):
        headers = {
            'Host': 'ptlogin.4399.com',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
            'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
            'Referer': 'http://ptlogin.4399.com/ptlogin/regFrame.do?regMode=reg_phone&postLoginHandler=default&redirectUrl=&displayMode=popup&css=&appId=www_home&gameId=&noEmail=false&regIdcard=false&autoLogin=false&cid=&aid=&ref=&level=0&mainDivId=popup_reg_div&includeFcmInfo=false&externalLogin=qq&fcmFakeValidate=true&expandFcmInput=true&v=1581571519226',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }
        params = {
            'xx': '1',
            'captchaId': 'captchaReqbe26a791e8c2635255'
        }
        result = self.Sess.get(url=self.url_captcha, headers=headers, params=params).content
        f = open('1.jpg', 'wb')
        f.write(result)
        f.close()
        print('yanzhengma')
        return self.Sess




if __name__ == '__main__':
    s4 = S4399GetCaptSpider()
    s4.main()
