# scrapy-jcy
爬取 http://www.ajxxgk.jcy.gov.cn/html/index.html 的公开文书
由于只是scrapy入门，所以用的最简单的方式进行爬取，然后写了shell脚本去执行 scrapy crawl spider
## 爬虫
### 获取列表中信息
列表信息
* 标题 title
* 链接 url
* 案件号 case_id

然后将爬取到的列表保存到json文件

### 获取详细文书内容
通过上述步骤json中读取列表中的url，get详情页面，再逐个爬取文书内容

## Todo
scrapy框架应该可以逐层往下爬，有空的时候改改
