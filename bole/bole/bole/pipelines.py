 # -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class BolePipeline(object):
    def open_spider(self, spider):
        print('开始运行程序==============')
        self.file = open("spider.json", "w")

    def process_item(self, item, spider):
        self.file.write(str(item) + "," + "\n")
        return item

    def close_spider(self, spider):
        self.file.close()
        print('结束程序================')