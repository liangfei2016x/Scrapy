# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DataokeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    img_url = scrapy.Field()
    describe = scrapy.Field()
    price = scrapy.Field()
    marketing_plan = scrapy.Field()
    price1 = scrapy.Field()
    sales_volume = scrapy.Field()
