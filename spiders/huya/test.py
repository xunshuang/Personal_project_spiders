#!/usr/bin/python3
# coding:utf-8
import sys
sys.path.insert(0, '../..')

from common.my_Spider import Spider
from selenium import webdriver
import time
from requests.cookies import RequestsCookieJar
from urllib.request import quote
import re
import json
import copy


class _Spider(Spider):
    def start_request(self):
        url = 'https://www.baidu.com'
        time.sleep(2)
        yield self.request('GET', url=url, finger=False, next_function=self.res)

    def res(self, req, resp):
        time.sleep(1)
        yield resp.text


if __name__ == '__main__':
    a = _Spider()
    a.crawl()
