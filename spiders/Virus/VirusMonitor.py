# coding:utf-8

import requests
import re
import parsel
import json
import random


class VirusSpider:
    def __init__(self):
        self.url = 'http://sa.sogou.com/new-weball/page/sgs/epidemic'

    def get_result(self):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Host': 'sa.sogou.com',
            'Pragma': 'no-cache',
            'Referer': 'https://www.sogou.com/web?query=%E7%96%AB%E6%83%85&_ast=1581062322&_asf=www.sogou.com&w=01029901&p=40040100&dp=1&cid=&s_from=result_up&sut=4822&sst0=1581062337224&lkt=0%2C0%2C0&sugsuv=1568693283360045&sugtime=1581062337224',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
        }
        params = {
            'type_page': 'pcpop'
        }
        result = requests.get(url=self.url, headers=headers, params=params)
        return result

    def parse_result(self, city):
        result = self.get_result().content.decode()
        result_dict = json.loads(re.findall('window.__INITIAL_STATE__ = (.*?)</script>', result, re.S)[0].strip())
        provinceNum = result_dict['data']['area']
        for i in provinceNum:
            for j in i['cities']:
                if j['cityName'] == city:
                    return {"确诊人数": j['confirmedCount'], "疑似人数": j['suspectedCount'], "治愈人数": j['curedCount'],
                            "死亡人数": j['deadCount']}

                elif city == i['provinceName']:
                    example = random.choice(i['cities'])['cityName']
                    return "{}可能为一个直辖市或者省份,如果是直辖市请重新输入区名,省份则输入城市,例如{}".format(city, example)

        return "所查询城市未找到记录"


if __name__ == '__main__':
    pass
