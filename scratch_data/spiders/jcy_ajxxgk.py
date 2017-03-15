# -*- coding: utf-8 -*-
import scrapy
from scratch_data.items import ScratchDataItem


class ZjxflwsSpider(scrapy.Spider):
    name = "zjxflws"
    allowed_domains = ["ajxxgk.jcy.gov.cn"]
    start_urls = ['http://www.ajxxgk.jcy.gov.cn/html/zjxflws/']
    #start_urls = start_urls + ['http://www.ajxxgk.jcy.gov.cn/html/zjxflws/%d.html' % i for i in range(2, 2722)] # 起诉书
    start_urls = start_urls + ['http://www.ajxxgk.jcy.gov.cn/html/zjxflws/%d.html' % i for i in range(2, 160)] # 不起诉书

    def parse(self, response):
        for sel in response.xpath('//*[@id="page_3"]/div/ul/li/div'):
            item = ScratchDataItem()
            item['title'] = sel.xpath('div[@class="ctitle"]/a[2]/@title').extract()
            item['url'] = sel.xpath('div[@class="ctitle"]/a[2]/@href').extract()
            item['case_id'] = sel.xpath('div[@class="ajh"]/a[1]/@title').extract()
            yield item


