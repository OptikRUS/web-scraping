# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductparserItem(scrapy.Item):
    _id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    site = scrapy.Field()
    img_urls = scrapy.Field()
    article = scrapy.Field()
    params = scrapy.Field()
