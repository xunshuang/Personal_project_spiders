#!/usr/bin/python3
# coding:utf-8
import re


class Header(object):
    def __init__(self):
        print('欢迎使用MS--1.0 Chrome请求头替换包')

    @staticmethod
    def header_replace(headers_raw, type=1):
        '''
        :param headers_raw: 原生请求头
        :param type: 类型，默认为1--Chrome
        :return:
        '''
        result = {}
        if type == 1:
            for i in headers_raw.splitlines():
                res = re.findall(pattern='^(.*?): (.*)', string=i)
                if res:
                    result[res[0][0].strip()] = res[0][1].strip()
            return result


if __name__ == '__main__':
    headers = '''
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cache-Control: no-cache
Connection: keep-alive
Cookie: SUV=1581062746986850; pgv_pvi=8157644800; cd=1581063776&1709597385e40fb4c2a7e6511c446c3f; sw_uuid=9475746084; sg_uuid=2874432239; ssuid=8717705640; CXID=FF6850057D6308FD0F8CD0B567152C66; SUID=D7BEFB6E1620940A000000005D805C26; SNUID=6D87A1DAC0BA5ECC8C55F021C0938AAF; ad=Yp21tkllll2W5SLTlllllViVGQDlllllBSccryllllYlllllRFkin5@@@@@@@@@@; IPLOC=CN1310; pgv_si=s8357430272; sct=153; ld=Ckllllllll2W5SIOg01zzOip6WBW5SikBSccryllll1lllllRklll5@@@@@@@@@@; LSTMV=302%2C494; LCLKINT=6286
Host: sa.sogou.com
Pragma: no-cache
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36
    '''
    a = Header.header_replace(headers_raw=headers)
    print(a)
