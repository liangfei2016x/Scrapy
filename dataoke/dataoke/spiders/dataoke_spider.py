import scrapy
import re
from dataoke.items import DataokeItem

class DmozSpider(scrapy.Spider):
    name = "dataoke"
    allowed_domains = ["http://www.dataoke.com/"]
    start_urls = [
        "http://www.dataoke.com/qlist/?page=1"
    ]

    def parse(self, response):
        for sel in response.xpath('//*[@class="goods-list clearfix"]/div/div'):
            item = DataokeItem()
            item["img_url"] = sel.xpath("div[1]/a/img/@src").extract_first()
            item["describe"] = re.sub("[\n\t]", "", sel.xpath("div[2]/span/a/text()").extract_first())
            item["price"] = sel.xpath("div[2]/div[2]/div[1]/p/b/text()").extract_first()
            item["marketing_plan"] = sel.xpath("div[2]/div[2]/div[2]/p/text()").extract_first()
            item["price1"] = sel.xpath("div[2]/div[3]/div[1]/p/b/text()").extract_first()
            item["sales_volume"] = sel.xpath("div[2]/div[3]/span/b/text()").extract_first()
            yield item
        # 分页数据 从第二页抓起
        totalPage = response.xpath('/html/body/div[3]/div[2]/div[2]/div/div[2]/b[1]/text()').extract_first().replace('/', '')
        pageNum = response.xpath('//div[@class="quan_page_main"]/span[@class="cur"]/text()').extract_first()
        next_num = int(pageNum) + 1
        if next_num <= int(totalPage):
            new_url = 'http://www.dataoke.com/qlist/?page={}'.format(str(next_num))
            yield scrapy.Request(new_url, callback=self.parse, dont_filter=True)


