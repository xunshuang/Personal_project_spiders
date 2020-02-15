# coding:utf-8

import requests
import datetime
from common.headers_replace import Header
from common.my_Spider import Spider
import re
import parsel
import json
import random


class VirusSpider(Spider):
    def start_request(self):
        url = 'http://sa.sogou.com/new-weball/page/sgs/epidemic'
        headers = '''
        Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3
        Accept-Encoding: gzip, deflate
        Accept-Language: zh-CN,zh;q=0.9
        Cache-Control: no-cache
        Connection: keep-alive
        Host: sa.sogou.com
        Pragma: no-cache
        Upgrade-Insecure-Requests: 1
        User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36
        '''
        headers = Header.header_replace(headers_raw=headers)
        yield self.request('GET', url=url, headers=headers, next_function=self.parse, UA=True)

    def parse(self, req, resp):
        result_dict = json.loads(
            re.findall('window.__INITIAL_STATE__ = (.*?)</script>', resp.content.decode(), re.S)[0].strip())
        city_info = {}
        news_info = []
        """
        :type = 1 城市查询
        :type = 2 省份或者直辖市查询
        :type = 3 国家查询
        """
        type = self.task.get('type', '')
        place = self.task.get('place', '')
        if int(type) == 1:
            for i in result_dict['data']['area']:
                for j in i['cities']:
                        if place == j['cityName']:
                            city_info = j
                            try:
                                del city_info['message']
                            except:
                                pass
                            break
                        else:
                            city_info['message'] = '所查询区域无可用信息'
        elif int(type) == 2:
            for i in result_dict['data']['area']:
                if place == i['provinceName'] or place == i['preProvinceName']:
                    city_info['cityName'] = i['provinceName']
                    city_info['confirmedCount'] = i['confirmedCount']
                    city_info['suspectedCount'] = i['suspectedCount']
                    city_info['curedCount'] = i['curedCount']
                    city_info['deadCount'] = i['deadCount']
                    try:
                        del city_info['message']
                    except:
                        pass
                    break
                else:
                    city_info['message'] = '所查询区域无可用信息'

        elif int(type) == 3:
            for i in result_dict['data']['overseas']:
                if place == i['provinceName'] or place == i['preProvinceName']:
                    city_info['cityName'] = i['provinceName']
                    city_info['confirmedCount'] = i['confirmedCount']
                    city_info['suspectedCount'] = i['suspectedCount']
                    city_info['curedCount'] = i['curedCount']
                    city_info['deadCount'] = i['deadCount']
                    try:
                        del city_info['message']
                    except:
                        pass
                    break
                else:
                    city_info['message'] = '所查询区域无可用信息'

        for i in result_dict['data']['timeline']['list']:
            info = {}
            info['title'] = i['title']
            info['content'] = i['content']
            news_info.append(info)

        now_time = re.findall('^(.*?)\.',str(datetime.datetime.now()))[0]

        return city_info,news_info,now_time





if __name__ == '__main__':
    a = VirusSpider()
    a.task = {'place': '廊坊', 'type': '1'}
    a.crawl()
