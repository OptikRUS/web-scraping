import scrapy


class VcItem(scrapy.Item):
    _id = scrapy.Field()
    user = scrapy.Field()
    user_id = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    img_url = scrapy.Field()
