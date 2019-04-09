# -*- coding: utf-8 -*-
import scrapy
from ..items import BoleItem
from scrapy_redis.spiders import RedisSpider

class BoleSpiderSpider(RedisSpider):
    name = 'bole_spider'
    # allowed_domains = ['sss']
    # start_urls = ['http://blog.jobbole.com/all-posts//']
    redis_key = 'bole:start_urls'

    def parse(self, response):
        index_page_change = 3
        detail_url_list = response.xpath('//a[@class="archive-title"]/@href').extract()
        index_num = response.xpath('//span[@class="page-numbers current"]/text()').extract()
        if detail_url_list:
            for detail_url in detail_url_list:
                yield scrapy.Request(url=detail_url, callback=self.detail_parse)
        else:
            print('========url获取异常')
        if index_num:
            if index_num < index_page_change:
                index_num += 1
                change_url = 'http://blog.jobbole.com/all-posts/page/{}/'.format(index_num)
                yield scrapy.Request(url=change_url, callback=self.parse)
        else:
            print('=========翻页异常')


    def detail_parse(self, response):
        items = BoleItem()
        name = response.xpath('//h1/text()').extract()[0]
        time = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract()[0].replace('"','').strip()
        author = response.xpath('//div[@class="copyright-area"]/a[1]/text()').extract()[0]
        if name:
            items['name'] = name
        if time:
            items['time'] = time
        if author:
            items['author'] = author
        yield items
