# -*- coding: utf-8 -*-
import scrapy
from ..items import SinaIaskItem

class SinaSpiderSpider(scrapy.Spider):
    name = 'sina_spider'
    # allowed_domains = ['https://iask.sina.com.cn/c/74.html']
    start_urls = ['https://iask.sina.com.cn/c/74.html']

    def parse(self, response):
        next_url = 'https://iask.sina.com.cn' + response.xpath('//a[@class="btn-page"]/@href').extract()[0]
        detail_url_list = response.xpath('//div[@class="question-title"]/a/@href').extract()
        if detail_url_list:
            for i in detail_url_list:
                detail_url = 'https://iask.sina.com.cn' + i
                yield scrapy.Request(url=detail_url, callback=self.detail_parse)
        if next_url:
            yield scrapy.Request(url=next_url, callback=self.parse)

    def detail_parse(self, response):
        items = SinaIaskItem()
        question = response.xpath('//pre[@class="question-text"]/text()').extract()
        answer_List = response.xpath('//ul[@class="new-answer-list"]/li')
        if question:
            items['question'] = question
        if not answer_List:
            return None
        for answer_index in answer_List:
            answer_time = answer_index.xpath('.//p[@class="time"]/text()').extract()[0]
            answer = answer_index.xpath('.//pre/text()').extract()[0]
            answer_person = answer_index.xpath('.//p[@class="user-name"]/a/text()').extract()[0]
            if answer:
                items['answer'] = answer
            if answer_person:
                items['answer_person'] = answer_person
            if answer_time:
                items['answer_time'] = answer_time
        return items