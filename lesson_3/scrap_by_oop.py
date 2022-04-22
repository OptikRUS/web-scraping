from pymongo import MongoClient

from lesson_2.vacanсies_scrapper import VacancyScrapper
from lesson_2.vacanсies_scrapper_sj import SuperJobVacancyScrapper


class AddNewVacanciesHH(VacancyScrapper):
    mongo_host = "localhost"
    mongo_port = 27017
    mongo_db = "all_vacancies"
    mongo_collection = "hh_vacancies"

    def save_vacancy_info(self):
        self.run()
        with MongoClient(self.mongo_host, self.mongo_port) as client:
            db = client[self.mongo_db]
            collection = db[self.mongo_collection]
            count = 0
            for vacancy in self.all_vacancy:
                if collection.find_one(vacancy):
                    pass
                else:
                    collection.insert_one(vacancy)
                    count += 1
        print(f'added {count} new vacancies')


class AddNewVacanciesSJ(AddNewVacanciesHH, SuperJobVacancyScrapper):
    mongo_collection = "sj_vacancies"
