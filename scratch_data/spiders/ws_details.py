# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import scrapy
import re
import json
import os
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor


class WsDetailsSpider(scrapy.Spider):
    name = "ws_details"
    allowed_domains = ["ajxxgk.jcy.gov.cn"]

    def __init__(self, **kw):
        json_path = kw.get('json_path')
        self.save_dir = kw.get('save_dir', 'data/other')
        self.start_urls = []
        f = open(json_path, "r")
        json_file = f.read()
        f.close()
        url_json = json.loads(json_file)
        for item in url_json:
            url = "http://www.ajxxgk.jcy.gov.cn" + item["url"][0]
            self.start_urls.append(url)

    def parse(self, response):
        save_dir = response.url.split("/")[-3]
        m = re.match("(\d+).html", response.url.split("/")[-1])
        index = 0
        if m:
            filename = m.group(1)
        else:
            filename = 'noindex%d' % index
            index += 1
        path = os.path.join(self.save_dir, save_dir)
        if not os.path.exists(path):
            os.makedirs(path)
        path = os.path.join(path, filename)
        ws = []
        text_pgs = response.xpath('//*[@id="contentArea"]/div/p')
        for sel in text_pgs:
            paragraph = sel.xpath('.//text()').extract()
            paragraph = ''.join(paragraph)
            paragraph = re.sub('\s+', '', paragraph)
            #paragraph = re.sub('\xC2\xA0', '', paragraph)
            if paragraph != '':
                ws.append(paragraph)
        text = '\n'.join(ws)

        f = open(path, "w")
        f.write(text)
        f.close()