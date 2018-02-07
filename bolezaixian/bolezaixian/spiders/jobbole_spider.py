# -*- coding: utf-8 -*-
# import sys
# import io
import scrapy
import time
from bolezaixian.items import BolezaixianItem
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='GBK')


class JobboleSpider(scrapy.Spider):
    name = "jobbole"
    allowed_domains = ["http://blog.jobbole.com"]
    start_urls = ["http://blog.jobbole.com/all-posts/"]

    def parse(self, response):
        post_nodes = response.xpath('// *[ @ id = "archive"] / div / div[1]')
        for post_node in post_nodes:
            item = BolezaixianItem()
            post_url = post_node.xpath("a/@href").extract_first()
            image_url = post_node.xpath("a/img/@src").extract()
            print(post_url, image_url)
            item["picture_url"] = image_url
            yield scrapy.Request(url=post_url, meta={'item': item}, callback=self.parse_detail, dont_filter=True)
        next_page = response.css('.next.page-numbers::attr(href)').extract_first()
        time.sleep(5)
        print("当前页链接："+next_page)
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse, dont_filter=True)

    def parse_detail(self, response):
        item = response.meta['item']
        create_date = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract_first()
        tags = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/a/text()').extract()
        title = response.xpath('//div[@class="entry-header"]/h1/text()').extract_first()
        h3 = response.xpath('//div[@class="entry"]/h3/text()').extract_first()
        contents = response.xpath('//div[@class="entry"]/p/text()').extract()
        content = h3 + "," + "".join(contents) if h3 else "".join(contents)
        tag = '.'.join(tags)
        item["title"] = title
        item["content"] = content
        item["tag"] = tag
        item["create_date"] = create_date
        yield item




