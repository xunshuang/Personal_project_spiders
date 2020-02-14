#!/usr/bin/python3
# coding:utf-8
import requests


class S4399PostCaptSpider:
    def __init__(self):
        self.url_post = 'http://ptlogin.4399.com/ptlogin/sendRegPhoneCode.do'

    def post_captcha(self, capt_number, phone_number):
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
            'phone': phone_number,
            'appId': 'www_home',
            'v': '3',
            'sig': '1581571518878dffa064',
            'captchaId': 'captchaReqbe26a791e8c2635255',
            'captcha': capt_number,
            'v': '1',
        }
        self.Sess.get(url=self.url_post, headers=headers, params=params)

    def main(self, Sess):
        self.get_captcha()
        capt_number = input()
        self.post_captcha(capt_number, phone_number='15566528051')
