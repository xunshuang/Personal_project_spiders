#!/usr/bin/python3
# coding:utf-8

from common.my_Spider import Spider
from selenium import webdriver
import time
from requests.cookies import RequestsCookieJar
import json
from urllib.request import quote
import re


class HuyaSpider(Spider):
    def start_request(self):
        f = open('danmu.txt', 'w', encoding='utf-8')
        f.write('弹幕分割线')
        try:
            self.option = webdriver.ChromeOptions()
            self.option.add_argument('--no-sandbox')
            self.option.add_argument('--disable-dev-shm-usage')
            # self.option.add_argument('--headless')
            self.option.add_argument('--disable_gpu')
            self.option.add_experimental_option('excludeSwitches', ['enable-automation'])
            # driver = webdriver.Chrome(executable_path='/root/chrome/chromedriver', options=self.option)
            self.driver = webdriver.Chrome(options=self.option)
            self.driver.get('https://www.huya.com/')
            self.driver.find_element_by_xpath('//*[@id="nav-login"]').click()
            time.sleep(3)
            self.driver.switch_to.frame(self.driver.find_elements_by_tag_name('iframe')[0])
            username = self.driver.find_element_by_xpath('//*[@id="account-login-form"]/div[1]/input')
            username.send_keys(f'{self.task["username"]}')
            password = self.driver.find_element_by_xpath('//*[@id="account-login-form"]/div[2]/input')
            password.send_keys(f'{self.task["password"]}')
            time.sleep(1)
            self.driver.find_element_by_xpath('//*[@id="login-btn"]').click()
            time.sleep(3)
            name = self.driver.find_element_by_xpath('//*[@id="login-username"]').text
            print('username:{}登录成功'.format(name))
            cookie = RequestsCookieJar()
            for i in self.driver.get_cookies():
                cookie.set(name=i['name'], value=i['value'])

            url = "https://search.cdn.huya.com/?callback=jQuery111108500719688812345_15832323495073261333333&m=Search&do=getSearchContent&q={}&uid=0&v=4&typ=-5&livestate=0&rows=16&_=15834950732663434".format(
                quote(f'{self.task["keyword"]}'))
            headers = {
                'accept': '*/*',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'zh-CN,zh;q=0.9',
                'referer': 'https://www.huya.com/search?hsk=%E9%9D%92%E8%9B%99',
                'authority': 'search.cdn.huya.com',
                'sec-fetch-dest': 'script',
                'sec-fetch-mode': 'no-cors',
                'sec-fetch-site': 'same-site',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36',
            }

            yield self.request('GET', url=url, headers=headers, next_function=self.enter_room, cookie=cookie)
        except:
            print('登陆失败！')
            print('二号方案启动')
            self.driver.get('https://www.huya.com/')
            cookie = RequestsCookieJar()
            for i in self.driver.get_cookies():
                cookie.set(name=i['name'], value=i['value'])
            # self.driver.close()
            url = "https://search.cdn.huya.com/?callback=jQuery111108500719688812345_15832323495073261333333&m=Search&do=getSearchContent&q={}&uid=0&v=4&typ=-5&livestate=0&rows=16&_=15834950732663434".format(
                quote(f'{self.task["keyword"]}'))
            headers = {
                'authority': 'search.cdn.huya.com',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36',
                'sec-fetch-dest': 'script',
                'accept': '*/*',
                'sec-fetch-site': 'same-site',
                'sec-fetch-mode': 'no-cors',
                'referer': 'https://www.huya.com/search?hsk=%E9%9D%92%E8%9B%99',
                'accept-language': 'zh-CN,zh;q=0.9',
                # 'cookie': 'udb_guiddata=333d396fc817400ca140f813eb7f20a6; __yamid_new=C8D179FDF860000137C97B602ED51811; __yamid_tt1=0.6316565836833095; SoundValue=0.50; udb_accdata=15566528051; udb_biztoken=AQBaGg2fK8dBDRh2NCrOPHwHkYA06fFOwOw99wL72ZuNSekySZAF1xSRJPcgUwE83GnovRiDb_h1eNIrwth8eRRhHoK7W1JdzuWjLBEqBqlJGdy2gy8GEiOHeqBpYOPY8CmaV1KESm004GWCEoKy5U0BvVMcSH8vWwTAJbRrSUY7szKnMjtPuavrpOVodE7pOtTKJMg04Kvj1frXD8d5IrTheDyfJSkWtoPnNkvjdvLrrCN-smPBKK0Ud0t8CSfXMQTm3Vlg58MmpdisCV0yy99gI77xnEy_hsUB3k-yGQHAY4Eur8BNShOtg4loO-2Z6Reg7jYLdepyF6AsUxk1QOYU; udb_origin=100; udb_other=%7B%22lt%22%3A%221583485946493%22%2C%22isRem%22%3A%221%22%7D; udb_passport=newqq_lyptwjynm; udb_status=1; udb_uid=1636781986; udb_version=1.0; username=newqq_lyptwjynm; yyuid=1636781986; h_unt=1583494293; udb_passdata=3; __yasmid=0.6316565836833095; __yaoldyyuid=1636781986; _yasids=__rootsid%3DC8D185058A50000160C94E201B4AF050; ya_rso=huya_h5_395; alphaValue=0.80; guid=0acf07579e34625e6b047a407b4051ec; Hm_lvt_51700b6c722f5bb4cf39906a596ea41f=1581923952,1583482142,1583494294,1583494349; isInLiveRoom=true; hiido_ui=0.022450381476243786; rep_cnt=6; huya_flash_rep_cnt=44; Hm_lpvt_51700b6c722f5bb4cf39906a596ea41f=1583494814; huya_web_rep_cnt=141',

            }

            yield self.request('GET', url=url, headers=headers, next_function=self.enter_room, cookies=cookie)

    def enter_room(self, req, resp):
        messages = json.loads(
            re.sub('jQuery\d+_\d+', '', resp.text).replace('(', '').replace(')', '').replace(';', '').replace('\n', ''))
        room_infos = messages['response']['1']['docs'][0]  # 默认第一个
        target_url = room_infos['game_liveLink']
        self.driver.get(url='https://www.huya.com/11342412')
        print('线程暂停3s')
        time.sleep(3)

        try:
            self.driver.find_element_by_xpath('//*[@id="player-ctrl-wrap"]/div[3]').click()
        except:
            pass
        print('线程暂停3s')
        time.sleep(3)
        messages_flag = []

        try:
            while True:
                messages = self.driver.find_elements_by_xpath('//*[@id="danmudiv"]/div/span')

                if len(messages):
                    for i in messages:
                        msg = i.text
                        if msg not in messages_flag:
                            print(msg)
                            f = open('danmu.txt', 'a+', encoding='utf-8')
                            f.write(msg + '\n')

                            messages_flag.append(msg)

                        else:
                            pass
                    time.sleep(2)
                else:
                    continue
        except:
            self.driver.quit()


if __name__ == '__main__':
    a = HuyaSpider()
    a.task = {
        'keyword': '周星驰',
        'username': '15566528051',
        'password': 'echo636474824..'
    }
    a.crawl()
