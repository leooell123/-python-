import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_dushu.items import ScrapyDushuItem

class ReadSpider(CrawlSpider):
    name = "read"
    allowed_domains = ["www.dushu.com"]
    #首页读取不到因为该地址不符号正则的规则
    # start_urls = ["https://www.dushu.com/book/1078.html"]
    start_urls = ["https://www.dushu.com/book/1078_1.html"]

    rules = (Rule(LinkExtractor(allow=r"/book/1078_\d+\.html"),
                  callback="parse_item",
                  follow=True),
              )

    def parse_item(self, response):
        item = {}
        # print("==============================")
        liList=response.xpath('//div[@class="bookslist"]/ul/li')
        for li in liList:
            src=li.xpath('.//a/img/@data-original').extract_first()
            title=li.xpath('.//h3/a/@title').extract_first()
            author=li.xpath('.//p[1]/text()').extract_first()
            print(src,title,author)
            book=ScrapyDushuItem(src=src,title=title,author=author)
            yield book

        # print(len(liList))
        #item["domain_id"] = response.xpath('//input[@id="sid"]/@value').get()
        #item["name"] = response.xpath('//div[@id="name"]').get()
        #item["description"] = response.xpath('//div[@id="description"]').get()
        return item
