import requests
# import re
from lxml import etree


# 生成类
class GetPage(object):
    def __init__(self, url):
        # 定义headers
        self.url = url
        self.ua = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
        }
        self.page = []
        self.id = []
        self.token = None

    # 获取页面数据
    def get_page(self):
        resp = requests.get(self.url, headers=self.ua)
        page = etree.HTML(resp.text)
        self.token = page.xpath('//meta[@content]/@content')[0]
        self.func(resp.text)

    # 获取ajax参数，加入headers
    def get_ajax(self, page):
        headers = {
            'x-csrf-token': self.token,
            'x-requested-with': 'XMLHttpRequest'
        }
        if page <=3:
            headers['x-infinitescroll'] = 'true'
        else:
            headers['x-pjax'] = 'true'
        headers.update(self.ua)
        params = {
            'seen_snote_ids[]': self.id,
            'page': page
        }
        resp = requests.get(self.url, headers=headers, params=params)
        self.func(resp.text)

    # 处理页面数据，存入列表
    def func(self, resp):
        page = etree.HTML(resp)
        result = page.xpath('//a[@class="title"]/text() | //p[@class="abstract"]/text()')
        # result = re.findall(r'<a class="title".*?>(.*?)</a>.*?<p class="abstract">(.*?)</p>', resp.text, re.S)
        self.page.extend(result)
        note_id = page.xpath('//li[@data-note-id]/@data-note-id')
        self.id.extend(note_id)

    # 运行程序
    def run(self):
        self.get_page()
        for i in range(2, 4):
            self.get_ajax(i)
        for j in self.page:
            print(j)


if __name__ == '__main__':
    A = GetPage('http://www.jianshu.com')
    A.run()