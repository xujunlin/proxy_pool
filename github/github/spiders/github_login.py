# -*- coding: utf-8 -*-
import scrapy
from ..settings import password

class GithubLoginSpider(scrapy.Spider):
    name = 'github_login'
    # allowed_domains = ['dddd']
    start_urls = ['https://github.com/login']

    def parse(self, response):
        url_login = 'https://github.com/session'
        authenticity_token = response.xpath('//input[@name="authenticity_token"]/@value').extract_first()
        data = {
            'commit': 'Sign in',
            'utf8': '✓',
            'authenticity_toke': 'authenticity_token',
            'login': 'xjl_dwy@163.com',
            'password': password,
            'authenticity_token': authenticity_token
        }
        yield scrapy.FormRequest(url=url_login, formdata=data, callback=self.login_after)

    def login_after(self, response):
        print(response.text)