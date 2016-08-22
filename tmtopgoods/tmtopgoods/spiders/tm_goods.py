# -*- coding: utf-8 -*-
import scrapy
from tmtopgoods.items import TmtopgoodsItem


class TmGoodsSpider(scrapy.Spider):
    name = "tm_goods"
    allowed_domains = ["tmall.com"]
    start_urls = (
        'https://list.tmall.com/search_product.htm?spm=a220m.1000858.0.0.navd8h&cat=50025135&sort=d&style=g&from=sn_1_cat-qp&active=1&industryCatId=50025135&type=pc',
    )

    def parse(self, response):
    	divs = response.xpath("//*[@id='J_ItemList']/div")
    	for div in divs:
        	item=TmtopgoodsItem()
        	item['GOODS_PRICE'] =div.xpath('div/p[1]/em/@title')[0].extract()
        	item['GOODS_NAME'] =div.xpath('div/p[2]/a/text()')[0].extract()
        	pre_goods_url = div.xpath('div/p[2]/a/@href')[0].extract()
        	item['GOODS_URL'] = pre_goods_url if "http:" in pre_goods_url else ("http:"+pre_goods_url)
        	picture_urls = div.xpath('div/div[1]/a/img/@src | div/div[1]/a/img/@data-ks-lazyload')[0].extract()
        	item['PICTURE_URL'] = ["http:"+picture_urls]

       		yield scrapy.Request(url=item['GOODS_URL'],meta={'item':item},callback=self.parse_detail,dont_filter=True)

    def parse_detail(self,response):
    	div=response.xpath('//*[@id="shopExtra"]/div[1]')
    	item = response.meta['item']
    	div=div[0]
    	item['SHOP_NAME'] = div.xpath('a/strong/text()')[0].extract()
    	shop_url = div.xpath('a/@href')[0].extract()
    	item['SHOP_URL'] = shop_url if "http:" in shop_url else ("http:"+shop_url)
    	yield item

"""
//*[@id="J_ItemList"]/div[1]/div
//*[@id="J_ItemList"]/div[1]
//*[@id="J_ItemList"]/div[2]/div
//*[@id="J_ItemList"]/div[2]/div/div[1]
//*[@id="J_ItemList"]/div[1]/div/p[1]/em
//*[@id="J_ItemList"]/div[1]/div/div[1]
//*[@id="J_ItemList"]/div[1]/div/div[1]/a/img
//*[@id="J_ItemList"]/div[2]/div/div[1]/a/img
//*[@id="J_ItemList"]/div[1]/div/p[1]
//*[@id="J_ItemList"]/div[1]/div/p[1]/em
//*[@id="J_ItemList"]/div[1]/div/p[2]/a
//*[@id="J_ItemList"]/div[1]/div/div[3]/a
//*[@id="shopExtra"]/div[1]/a/strong
//*[@id="shopExtra"]/div[1]/a
//*[@id="J_ItemList"]/div[1]/div/div[1]/a/img
//*[@id="J_ItemList"]/div[7]/div/div[1]/a/img
//*[@id="J_ItemList"]/div[60]/div/div[1]/a/img
//*[@id="J_ItemList"]/div[1]/div/div[1]/a/img
"""