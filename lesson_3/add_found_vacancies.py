from pymongo import MongoClient


def add_found_vacancies(scraper, mongo_host, mongo_port, mongo_db, mongo_collection):
    scraper.run()
    found_vacancies = scraper.all_vacancy
    with MongoClient(mongo_host, mongo_port) as client:
        db = client[mongo_db]
        collection = db[mongo_collection]
        count = 0
        for vacancy in found_vacancies:
            collection.insert_one(vacancy)
    print(f'added {count} new vacancies')
