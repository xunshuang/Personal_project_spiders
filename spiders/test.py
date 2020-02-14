from Personal_project_spiders.common.my_Spider import Spider


class A(Spider):
    def start_request(self):
        url = 'http://www.baidu.com'
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Cookie': 'BD_UPN=12314753; PSTM=1581572198; BAIDUID=581D183935D4F5B159942D0C2473C0D6:FG=1; BIDUPSID=33A41DCDCEEFD730F44D9A93E298A604; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; delPer=0; BD_CK_SAM=1; PSINO=2; WWW_ST=1581672040423; BD_HOME=0; H_PS_PSSID=',
            'Host': 'www.baidu.com',
            'Pragma': 'no-cache',
            'Referer': 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd=%40abc.abstractmethod&oq=cut%25E6%258C%2587%25E4%25BB%25A4&rsv_pq=e244d1c40000add2&rsv_t=af65RwGGdWCdSvh5iaA396Ag38iiiyS%2FCgKpBhUpTgdBDeMS759brTghB88&rqlang=cn&rsv_enter=1&rsv_dl=tb&inputT=1642&rsv_n=2&rsv_sug3=51&bs=cut%E6%8C%87%E4%BB%A4',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
        }
        yield self.request(url=url, method='GET', headers=headers, new_session=False, next_function=self.parse,proxy='USE')

    def parse(self, req, resp):
        return '1231321'


if __name__ == '__main__':
    a = A()
    a.crawl()
    print(a.result[0])
