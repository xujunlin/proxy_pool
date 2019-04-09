# -*- coding: utf-8 -*-
import scrapy
import requests
import re


class DoubanSpiderSpider(scrapy.Spider):
    name = 'douban_spider'
    # allowed_domains = ['dddd']
    start_urls = ['https://accounts.douban.com/login']

    def parse(self, response):
        '''

        :param response:
        :return:
        '''

        data = {
            'ck': 'C-2X',
            'source': 'None',
            'redir': 'https://www.douban.com/',
            'form_email': '1257051717@qq.com',
            'form_password': 'm1257051717',
            'login': '登录',
        }
        # print(response.text)
        captcha_id = response.xpath('//input[@name="captcha-id"]/@value').extract_first()
        if captcha_id:
            print('需要验证码========================={}'.format(captcha_id))
            captcha = response.xpath('//img[@id="captcha_image"]/@src').extract_first()
            print(captcha,'===========================')
            with open('captcha.jpg', 'wb') as f:
                f.write(requests.get(captcha).content)

            captcha_code = input("请输入验证码")
            data['captcha-solution'] = captcha_code
            data['captcha-id'] = captcha_id
        print('正在登入===========================')
        yield scrapy.FormRequest(url=self.start_urls[0], formdata=data, callback=self.login_after)

    def login_after(self, response):
        url = 'https://www.douban.com/'
        data = {
            'ck': 'c9ru'
        }
        comment = '就是爱学python++++'
        print('开始写日记')
        data['comment'] = comment
        yield scrapy.FormRequest(url=url, formdata=data, callback=self.reed_write, dont_filter=True)

    def reed_write(self, response):
        print(response.status)
        print(response.text,'=====================')
        # write = response.findall(r'.*?(就是爱学python).*?',response.text)
        # print(write)