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

    def process_salary(self, salary_list: list):
        if len(salary_list) == 1:
            return None, None, None
        elif len(salary_list) == 4:
            return int(salary_list[0].replace('\xa0', '')), int(salary_list[1].replace('\xa0', '')), salary_list[-1]
        elif len(salary_list) == 3:
            zp = salary_list[2].split('\xa0')
            return int(''.join(zp[0:2])), None, zp[2]
        elif len(salary_list) == 7:
            return int(salary_list[1].replace('\xa0', '')), int(salary_list[3].replace('\xa0', '')),  salary_list[-2]
        elif len(salary_list) == 5:
            if salary_list[0] == 'до ':
                return None, int(salary_list[1].replace('\xa0', '')), salary_list[-2]
            return int(salary_list[1].replace('\xa0', '')), None, salary_list[-2]
        else:
            return None, None, None

    def process_item(self, item, spider):
        salary_min, salary_max, salary_currency = self.process_salary(item['salary'])
        item['salary_min'] = salary_min
        item['salary_max'] = salary_max
        item['salary_currency'] = salary_currency
        item['site'] = spider.name
        item.pop('salary')
        collection = self.db[spider.name]
        collection.insert_one(item)
        print(item)
        return item
