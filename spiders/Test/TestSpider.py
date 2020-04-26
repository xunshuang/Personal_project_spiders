from common.MyRequests import MyRequests



class TestSpider(MyRequests):

    def start_request(self):
        url = "https://www.baidu.com"
        yield self.request(url=url,next_function=self.get_result)

    def get_result(self,req,resp):
        cookies = req['req'].cookies
        for i in cookies:
            print(i)
        url = "https://www.baidu.com/s"
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            # 'Cookie': 'BD_UPN=12314753; sug=3; sugstore=0; ORIGIN=0; bdime=0; BAIDUID=96ECDAA30AD79CF4FE3A263112AB1ED5:FG=1; BIDUPSID=33A41DCDCEEFD730F44D9A93E298A604; PSTM=1587376103; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; BDSFRCVID=WSkOJeC62wd-iU3u6D_MbH3ZlaB-8YTTH6aIwaLc4q8vRblzxXziEG0PeU8g0KubyhV6ogKKBmOTHgLF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=tJue_D-yfC-3fP36q4jqMt-8qxo-qhbg22OZ0l8Ktt3fKJTaDn_-Qh4I-4AeXt7K0tDOhxbmWIQHOt3pX--MKjkB0x5QhJvvMD54KKJx5xKWeIJo5t5BMh5BhUJiBMjLBan70hRIXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtpChbRO4-TF-D6c0jMK; delPer=0; BD_CK_SAM=1; PSINO=2; H_PS_645EC=e4d5LsDqmmmITmQLxHdlejSx01NDvJIAM8%2Bdp5y6nXQ3YXczqTOChHsU%2BWXphG3TECISehrArNnK; COOKIE_SESSION=4303_0_8_9_6_3_0_0_7_1_0_0_8787_0_229_0_1587883778_0_1587883549%7C9%23925319_35_1587874817%7C9; BD_HOME=1; H_PS_PSSID=30968_1422_31326_21121_31341_30823_31163; BDSVRTM=50; WWW_ST=1587884137129',
            'Host': 'www.baidu.com',
            'is_referer': 'https://www.baidu.com/',
            'is_xhr': '1',
            'Pragma': 'no-cache',
            'Referer': 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd=%E8%B6%85%E7%BA%A7&fenlei=256&rsv_pq=d33b4005000cbc90&rsv_t=2eb7PSOptQtb4Bm3EzLk%2Fe4W5fyVhw0jg%2FttGk0WtH%2Ba6RWd9WdKTDMYh%2FI&rqlang=cn&rsv_enter=0&rsv_dl=tb&rsv_sug3=8&rsv_sug1=6&rsv_sug7=100&rsv_btype=i&inputT=4979&rsv_sug4=7000',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }
        params = {
            'ie': 'utf-8',
            'mod': '1',
            'isbd': '1',
            'isid': '96ECDAB1ED519260',
            'ie': 'utf-8',
            'f': '8',
            'rsv_bp': '1',
            'rsv_idx': '1',
            'tn': 'baidu',
            'wd': '超级',
            'fenlei': '256',
            'rsv_pq': 'd33b4005000cbc90',
            'rsv_t': '2eb7PSOptQtb4Bm3EzLk/e4W5fyVhw0jg/ttGk0WtH+a6RWd9WdKTDMYh/I',
            'rqlang': 'cn',
            'rsv_enter': '0',
            'rsv_dl': 'tb',
            'rsv_sug3': '8',
            'rsv_sug1': '6',
            'rsv_sug7': '100',
            'rsv_btype': 'i',
            'inputT': '4979',
            'rsv_sug4': '7000',
            'rsv_sid': '30968_1422_31326_21121_31341_30823_31163',
            '_ss': '1',
            'clist': '',
            'hsug': '',
            'f4s': '1',
            'csor': '2',
            '_cr1': '32189',
        }
        yield self.request(url=url,headers=headers,params=params,next_function=self.parse)

    def parse(self,req,resp):
        print(req['req'].cookies)
        pass
        # print(resp.status_code)



if __name__ == '__main__':
    a = TestSpider()
    a.crawl()