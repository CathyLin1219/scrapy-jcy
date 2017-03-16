# -*- coding: utf-8 -*-
import scrapy, re
from scratch_data.items import ScratchDataItem


class ZjxflwsSpider(scrapy.Spider):
    name = "zjxflws"
    allowed_domains = ["ajxxgk.jcy.gov.cn"]
    start_urls = ['http://www.ajxxgk.jcy.gov.cn/html/zjxflws/']
    #start_urls = start_urls + ['http://www.ajxxgk.jcy.gov.cn/html/zjxflws/%d.html' % i for i in range(2, 2722)] # 起诉书
    start_urls = start_urls + ['http://www.ajxxgk.jcy.gov.cn/html/zjxflws/%d.html' % i for i in range(2, 3)] # 不起诉书

    def __init__(self, **kw):
        ws_type = kw.get('ws_type')
        self.date_limit = kw.get('date', None)
        if ws_type == 'all':
            page = '0'
        elif ws_type == 'qss':
            page = '1'
        elif ws_type == 'kss':
            page = '2'
        elif ws_type == 'bqsjds':
            page = '3'
        elif ws_type == 'xsssfcjds':
            page = '4'
        elif ws_type == 'qtflws':
            page = '6'
        else:
            page = ''
        self.xpath_pattern = '//*[@id="page_%s"]/div/ul/li/div' % page


    def parse(self, response):
        for sel in response.xpath(self.xpath_pattern):
            item = ScratchDataItem()
            item['title'] = sel.xpath('div[@class="ctitle"]/a[2]/@title').extract()
            item['url'] = sel.xpath('div[@class="ctitle"]/a[2]/@href').extract()
            item['case_id'] = sel.xpath('div[@class="ajh"]/a[1]/@title').extract()
            if self.date_limit == None or item['url'][0].split("/")[-3] == self.date_limit:
                yield item
