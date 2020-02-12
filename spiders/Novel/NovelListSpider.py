import requests
from lxml import etree


class NovelListSpider(object):
    """
    笔趣阁小说爬虫
    """

    def __init__(self):
        self.host = 'https://www.biqudu.net'
        self.Sess = requests.Session()
    def search_novel(self, keyword):
        url = self.host + '/searchbook.php'
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'referer': 'https://www.biqudu.net/0_2/733136.html',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
        }
        params = {
            'keyword': keyword
        }
        novels = self.Sess.get(url=url, headers=headers, params=params)
        return novels.content.decode()

    def select_novel(self, novels_html):
        novels_name = []  # 小说名字
        novels_writer = []  # 小说作者
        novels_sub = []  # 描述
        novels_id = []  # id
        novels_name_raw = novels_html.xpath(
            '//div[@id="main"]//div[@id="hotcontent"]//div[@class="item"]//img/@alt')
        novels_writer_raw = novels_html.xpath(
            '//div[@id="main"]//div[@id="hotcontent"]//div[@class="item"]//span/text()')

        novels_sub_raw = novels_html.xpath(
            '//div[@id="main"]//div[@id="hotcontent"]//div[@class="item"]//dd/text()')
        novels_id_raw = novels_html.xpath(
            '//div[@id="main"]//div[@id="hotcontent"]//div[@class="item"]//div[@class="image"]//a/@href')

        novels_name = novels_name_raw

        for i in novels_writer_raw:
            novels_writer.append(i.replace('\r', '').replace('\n', '').replace(' ', ''))

        for i in novels_sub_raw:
            novels_sub.append(i.replace('\r', '').replace('\n', '').replace(' ', ''))

        novels_id = novels_id_raw

        return novels_name, novels_writer, novels_sub, novels_id

    def main(self, keyword):
        novels = self.search_novel(keyword=keyword)
        novels_html = etree.HTML(novels)
        novels_name, novels_writer, novels_sub, novels_id = self.select_novel(novels_html)
        return novels_name, novels_writer, novels_sub, novels_id,self.Sess


if __name__ == '__main__':
    biqu = NovelListSpider()
    biqu.main('德玛西亚')
