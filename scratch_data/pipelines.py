# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.contrib.exporter import JsonLinesItemExporter
from datetime import datetime

class ScratchDataPipeline(object):
    def __init__(self):
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        return pipeline

    def open_spider(self, spider):
        print "===open_spider==="
        file = open('data/%s_products_%s.json' % (spider.name, datetime.now().strftime("%Y%m%d%H%M%S")), 'w+b')
        self.files[spider] = file
        self.exporter = JsonLinesItemExporter(file, ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        print "===close_spider==="
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        print "===process_item==="
        self.exporter.export_item(item)
        return item