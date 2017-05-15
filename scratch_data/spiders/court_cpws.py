# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest, Request
import json, time, random
from scratch_data.items import CpwsDataItem
from lxml import html

class CpwsSpider(scrapy.Spider):
    name = "cpws"
    allowed_domains = ["wenshu.court.gov.cn"]
    start_urls = ['http://wenshu.court.gov.cn/List/List?sorttype=1&conditions=searchWord+1++案件类型:刑事案件']
    start_urls = ['http://wenshu.court.gov.cn/CreateContentJS/CreateContentJS.aspx?DocID=1eb63d7a-412a-4504-87c3-a76f00993d4e']
    download_delay = 1
    concurrent_requests = 1

    def __init__(self):
        self.list_formdata = {"Param": "案件类型:刑事案件,文书类型:判决书",
                   "Index": '1',
                   "Page": '20',
                   "Order": '裁判日期',
                   "Direction": 'desc',
                   }
        self.list_url = "http://wenshu.court.gov.cn/List/ListContent"
        self.referer = CpwsSpider.start_urls[0]
        self.header = {
            'Host':"wenshu.court.gov.cn",
            'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
            'Accept':"*/*",
            'Accept-Language':"zh-CN,zh;q=0.8",
            'Accept-Encoding':"gzip, deflate",
            'Referer':self.referer,
            'Content-Type':"application/x-www-form-urlencoded; charset=UTF-8",
            'Connection':"keep-alive"
        }
        self.page_count = 0
        #scrapy.settings.BaseSettings.set('concurrent_requests', 1)

    def parse(self, response):
        print "in parse"
        # 第一次请求获取到有多少页数据
        try:
            yield FormRequest(url=self.list_url, callback=self.parse_page_cnt, method='POST',
                              formdata=self.list_formdata, headers=self.header, errback=self.proc_vertify, dont_filter = True)
        except Exception as e:
            print ('Error:getting item count failed!')
            print ('detail:', e)
            return


    def parse_page_cnt(self, response):
        print "in parse_page_cnt"
        #print response.text
        data = json.loads(json.loads(response.text))
        #print data
        self.page_count = int(data[0]['Count']) // 20

        # 逐页获取数据
        index = 1
        print 'page_count:%d' % self.page_count
        while index <= self.page_count:
            try:
                print '====index %d ====' % index
                self.list_formdata["Index"] = str(index)
                yield FormRequest(url=self.list_url, callback=self.parse_page_items, method='POST',
                                  formdata=self.list_formdata, headers=self.header, errback=self.proc_vertify, dont_filter = True)
                print "*****run to yield behind"
                time.sleep(random.random())  # 随机休眠一段时间
                index += 1
            except Exception as e:
                print ('Error:post index %d request failed!' % index)
                print ('detail:', e)
                file = open('last_index.cfg', 'w')
                file.write('%d' % index)
                file.close()
            break  # 跑一边尝试

    def parse_page_items(self, response):
        print "in parse_page_items"
        data = json.loads(json.loads(response.text))
        for i in range(1, len(data)):
            item = CpwsDataItem()

            item['wenshu_id'] = data[i][u'文书ID'].encode('utf-8')
            item['trial_round'] = data[i].get(u'审判程序',u'').encode('utf-8')
            item['case_title'] = data[i].get(u'案件名称',u'').encode('utf-8')
            item['judge_date'] = data[i].get(u'裁判日期',u'').encode('utf-8')
            item['case_number'] = data[i].get(u'案号',u'').encode('utf-8')
            item['case_court'] = data[i].get(u'法院名称',u'').encode('utf-8')
            item['case_type'] = data[i].get(u'案件类型',u'').encode('utf-8')
            item['cpyz'] = data[i].get(u'裁判要旨段原文',u'').encode('utf-8')
            yield item
            try:
                detail_url = 'http://wenshu.court.gov.cn/CreateContentJS/CreateContentJS.aspx?DocID={id}'.format(id=item['wenshu_id'])
                yield Request(url=detail_url, callback=self.parse_item_details, method='GET', dont_filter = True, meta={'wenshu_id':item['wenshu_id']})
            except Exception as e:
                print ('Error:get wenshu_id = %s failed!' % item['wenshu_id'])
                print ('detail:', e)


    def proc_vertify(self, spider):
        # todo处理验证码
        print "==处理验证码==Todo=="
        pass

    def parse_item_details(self, response):
        print "in parse_item_details"
        id = response.meta['wenshu_id']
        file = open('{id}.txt'.format(id=id), 'w')
        doc = html.document_fromstring(response.text)
        content = doc.xpath('//text()')
        content = ''.join(content[1:len(content) - 1])
        file.write(content)
        file.close()
