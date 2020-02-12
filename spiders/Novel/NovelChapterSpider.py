import requests
from lxml import etree


class NovelChapterSpider:
    """
    笔趣阁小说爬虫
    """

    def __init__(self):
        self.host = 'https://www.biqudu.net'

    def search_novel_id(self, Sess, novel_id):
        url = self.host + novel_id
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
        chapter = html.xpath('//div[@id="list"]//dd/a/text()')
        href = html.xpath('//div[@id="list"]//dd/a/@href')
        return chapter, href

    def main(self, Sess, novel_id):
        result = self.search_novel_id(Sess, novel_id)
        chapters, href = self.parse(result=result)
        return chapters[12:], Sess, href[12:]


if __name__ == '__main__':
    biqu = NovelChapterSpider()
    biqu.main('德玛西亚')
