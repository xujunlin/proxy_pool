import scrapy


class   Myscrapy(scrapy.Spider):
    name = 'spider'
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        print(response.text)