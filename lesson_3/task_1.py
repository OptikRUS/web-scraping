from lesson_2.vacanсies_scrapper import VacancyScrapper, URL as HH_URL, PARAMS as HH_PARAMS, HEADERS as HH_HEADERS
from lesson_2.vacanсies_scrapper_sj import SuperJobVacancyScrapper, URL as SJ_URL, PARAMS as SJ_PARAMS, \
    HEADERS as SJ_HEADERS
from add_new_vacancies import add_new_vacancies

MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DB = "all_vacancies"
MONGO_COLLECTION_HH = "hh_vacancies"
MONGO_COLLECTION_SJ = "sj_vacancies"

HH_PARAMS['text'] = input('Job title hh: ')
page_count_hh = input('number of pages hh: ')
SJ_PARAMS['keywords'] = input('Job title sj: ')
page_count_sj = input('number of pages sj: ')

hh_scraper = VacancyScrapper(HH_URL, HH_PARAMS, HH_HEADERS, page_count=page_count_hh)
sj_scraper = SuperJobVacancyScrapper(SJ_URL, SJ_PARAMS, SJ_HEADERS, page_count=page_count_sj)


add_new_vacancies(hh_scraper, MONGO_HOST, MONGO_PORT, MONGO_DB, MONGO_COLLECTION_HH)
add_new_vacancies(sj_scraper, MONGO_HOST, MONGO_PORT, MONGO_DB, MONGO_COLLECTION_SJ)
