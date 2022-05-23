import scrapy
from scrapy.pipelines.images import ImagesPipeline

from pymongo import MongoClient

MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DB = "readcity"


class BookparserPipeline:

    def __init__(self):
        self.client = MongoClient(MONGO_HOST, MONGO_PORT)
        self.db = self.client[MONGO_DB]

    def process_price(self, price: str):
        if price:
            only_num = price[:price.rfind(' ')]
            return float(only_num)
        else:
            return None

    def process_params(self, params: list) -> dict:
        res = {}
        for i in range(0, len(params) + 1, 2):
            try:
                res[params[i]] = params[i+1]
            except IndexError:
                pass
        return res

    def process_item(self, item, spider):
        item['params'] = self.process_params(item['params'])
        item['price'] = self.process_price(item['price'])
        collection = self.db[spider.name]
        collection.update_one(item, {"$set": item}, upsert=True)
        item['site'] = spider.name
        return item


class ProductparserImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item["img_urls"]:
            for img_url in item["img_urls"]:
                try:
                    yield scrapy.Request(img_url)
                except Exception as e:
                    print(e)
