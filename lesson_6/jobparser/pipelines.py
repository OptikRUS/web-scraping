# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient

MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DB = "jobs"


class JobparserPipeline:

    def __init__(self):
        self.client = MongoClient(MONGO_HOST, MONGO_PORT)
        self.db = self.client[MONGO_DB]

    def process_salary(self, slary_list: list):
        if 'от ' in slary_list:
            min_s = slary_list[slary_list.index('от ') + 1]
        else:
            min_s = None
        if ' до ' in slary_list:
            max_s = slary_list[slary_list.index(' до ') + 1]
        elif 'до ' in slary_list:
            max_s = slary_list[slary_list.index('до ') + 1]
        else:
            max_s = None
        if "з/п не указана" in slary_list:
            cur = None
        else:
            cur = slary_list[-2]

        return min_s, max_s, cur

    def process_item(self, item, spider):
        slary_min, salary_max, salary_currency = self.process_salary(item['salary'])
        print(slary_min, salary_max, salary_currency)
        if slary_min:
            item['slary_min'] = slary_min
        if salary_max:
            item['salary_max'] = salary_max
        if salary_currency:
            item['salary_currency'] = salary_currency
        item.pop('salary')
        collection = self.db[spider.name]
        collection.insert_one(item)
        return item
