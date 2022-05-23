import scrapy
from scrapy.loader.processors import Compose, MapCompose, TakeFirst


def get_big_img_urls(img_url: str):
    return img_url.replace('_82', '_2000')


class ProductparserItem(scrapy.Item):
    _id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    site = scrapy.Field()
    img_urls = scrapy.Field(input_processor=MapCompose(get_big_img_urls))
    img_info = scrapy.Field()
    article = scrapy.Field()
    params = scrapy.Field()
