import requests
from lxml import etree


class NovelContentSpider:
    """
    笔趣阁小说爬虫
    """

    def __init__(self):
        self.host = 'https://www.biqudu.net'

    def search_content(self, Sess, content_id):
        url = self.host + content_id
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
        }
        result = Sess.get(url=url, headers=headers).content.decode()
        return result

    def parse(self, result):
        html = etree.HTML(result)
        text = html.xpath('//div[@id="content"]/text()')
        return text

    def main(self, Sess, content_id):
        result = self.search_content(Sess, content_id)
        text_raw = self.parse(result=result)
        text = []
        for i in text_raw:
            text.append(i)
        return text


if __name__ == '__main__':
    biqu = NovelContentSpider()
    biqu.main('德玛西亚')
