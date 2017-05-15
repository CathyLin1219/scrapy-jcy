# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScratchDataItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    url =scrapy.Field()
    case_id = scrapy.Field()


class CpwsDataItem(scrapy.Item):
    wenshu_id = scrapy.Field()  # "文书ID": "8951a4e3-7425-407a-acb3-ce0e16f9e062",
    case_type = scrapy.Field()  # "案件类型": "1",
    judge_date = scrapy.Field() # "裁判日期": "2011-04-28",
    case_title = scrapy.Field()  # "案件名称": "王某交通肇事罪一审刑事判决书",
    trial_round = scrapy.Field()  # "审判程序": "一审",
    case_number = scrapy.Field()  # "案号": "（2011）嘉平刑初字第179号",
    case_court = scrapy.Field()  # "法院名称": "浙江省高级人民法院"
    cpyz = scrapy.Field()  # "裁判要旨段原文": "本院认为：被告人王某违反交通运输管理法规，发生重大交通事故，致一人死亡，其行为已构成交通肇事罪。公诉机关指控的罪名成立，应予支持。被告人王某在发生事故后，保护好现场并主动报警，如实向公安机关供述了自己的犯罪事实属自首，依法可以从轻处罚；同时，案发后，被告人积极要求家属设法筹款，给被害人家属额外进行补偿，有一定的悔罪表现，因此得到了被害人家属的谅解，亦可对被告人王某酌情从轻处罚。综上，对被告人王某从轻处罚并可适用缓刑。辩护人对此提出的辩护意见有理，本院予以采纳。据此，为惩治犯罪，依照《中华人民共和国刑法》第一百三十三条、第六十七条第一款、第七十二条第一款之规定，判决如下",






