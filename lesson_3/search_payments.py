from pprint import pprint

from pymongo import MongoClient
"""
Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы. 
Необязательно - возможность выбрать вакансии без указанных зарплат.
"""


MONGO_COLLECTION_HH = "hh_vacancies"
MONGO_COLLECTION_SJ = "sj_vacancies"


def search_payments(mongo_collection, payment_size=None):
    mongo_host = "localhost"
    mongo_port = 27017
    mongo_db = "all_vacancies"
    with MongoClient(mongo_host, mongo_port) as client:
        db = client[mongo_db]
        collection = db[mongo_collection]
        if payment_size:
            cursor = collection.find({
                "$and": [
                    {"vacancy_payments": {"$ne": None}},
                    {"$or": [
                        {"vacancy_payments.max": {"$gte": int(payment_size)}},
                        {"vacancy_payments.max": {"$gte": int(payment_size)}}
                    ]}
                ]
            })
            return list(cursor)
        else:
            cursor = collection.find({"$or": [{"vacancy_payments": None}, {"vacancy_payments": {"$type": "string"}}]})
            return list(cursor)


size_payments = input('Pay size: ')

pprint(search_payments(MONGO_COLLECTION_HH, size_payments))
pprint(search_payments(MONGO_COLLECTION_SJ, size_payments))
