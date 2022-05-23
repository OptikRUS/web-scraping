import scrapy
from scrapy.loader.processors import Compose, TakeFirst


def clean_strings(string_array):
    return [s.strip() for s in string_array]


def convert_to_float(rate_array):
    return [float(i) for i in rate_array]


class BookparserItem(scrapy.Item):
    _id = scrapy.Field()
    url = scrapy.Field(output_processor=TakeFirst())
    title = scrapy.Field(input_processor=Compose(clean_strings), output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst())
    site = scrapy.Field()
    img_urls = scrapy.Field()
    rate = scrapy.Field(input_processor=Compose(convert_to_float), output_processor=TakeFirst())
    annotation = scrapy.Field(input_processor=Compose(clean_strings), output_processor=TakeFirst())
    author = scrapy.Field(input_processor=Compose(clean_strings), output_processor=TakeFirst())
    params = scrapy.Field(input_processor=Compose(clean_strings))
