import json
from time import sleep
import re
from pprint import pprint

import requests
from bs4 import BeautifulSoup

URL = 'https://rostov.hh.ru/search/vacancy'
PARAMS = {
    'text': '',
    'page': 0, 'limit': 20,
    'hhtmFrom': 'vacancy_search_list'
}
HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10"}


class VacancyScrapper:
    def __init__(self, url, params, headers, page_count=None):
        self.headers = headers
        self.url = url
        self.start_params = params
        self.start_page_count = page_count
        self.all_vacancy = []

    def get_html_string(self, params):
        try:
            response = requests.get(url=self.url, params=params, headers=self.headers)
            response.raise_for_status()
        except Exception as e:
            sleep(1)
            print(e)
            return None
        return response.text

    @staticmethod
    def get_dom(html_string):
        return BeautifulSoup(html_string, "html.parser")

    @staticmethod
    def compile_str(str_zp):
        return re.compile(r'\d+\u202f\d+|\d+').findall(str_zp)[0].encode("ascii", "ignore").decode()

    def get_vacancy_name(self, element):
        h3 = element.h3
        if h3:
            return h3.text
        return None

    def get_vacancy_url(self, element):
        a = element.a
        if a:
            return a['href'][:a['href'].rfind('?')]
        return None

    def get_vacancy_pay(self, element):
        pay_element = element.findChild('span', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'})
        if pay_element:
            return pay_element.text
        return None

    def compile_payment(self, str_zp):
        if str_zp:
            zp_charcode = str_zp[str_zp.rfind(' ') + 1:]
            if str_zp.startswith('от'):
                min_zp = VacancyScrapper.compile_str(str_zp)
                max_zp = None
                return [min_zp, max_zp, zp_charcode]
            elif str_zp.startswith('до'):
                min_zp = None
                max_zp = VacancyScrapper.compile_str(str_zp)
                return [min_zp, max_zp, zp_charcode]
            else:
                range_zp = re.split(r' – ', str_zp)
                min_zp = re.compile(r'\d+\u202f\d+|\d+').findall(range_zp[0])[0].encode("ascii", "ignore").decode()
                max_zp = re.compile(r'\d+\u202f\d+|\d+').findall(range_zp[1])[0].encode("ascii", "ignore").decode()
                return [min_zp, max_zp, zp_charcode]
        else:
            return None

    def get_vacancy_employer(self, element):
        employer_element = element.findChild('div', attrs={'class': 'vacancy-serp-item__info'})
        if employer_element:
            return employer_element.text
        return None

    def get_vacancy_requirements(self, element):
        requirements_element = element.findChild('div', attrs={'class': 'g-user-content'})
        if requirements_element:
            return requirements_element.text
        return None

    def get_info_from_element(self, element):
        info = {}
        try:
            info['vacancy_payments'] = self.compile_payment(self.get_vacancy_pay(element))
            child = element.findChild('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'})
            if child:
                info['vacancy_name'] = self.get_vacancy_name(element)
                info['vacancy_url'] = self.get_vacancy_url(element)
                info['employer'] = self.get_vacancy_employer(element)
                info['requirements'] = self.get_vacancy_requirements(element)
                info['vacancy_site'] = 'hh.ru'
        except ValueError as e:
            print(e)
        return info

    def save_vacancy_info(self):
        with open(PARAMS['text'], 'w', encoding='utf-8') as f:
            json.dump(self.all_vacancy, f, indent=4)

    def process_page(self, params):
        html_string = self.get_html_string(params)
        if html_string is None:
            print("There was an error")
            return

        soup = VacancyScrapper.get_dom(html_string)
        vacancy_elements = soup.find_all('div', attrs={'class': 'vacancy-serp-item'})

        for element in vacancy_elements:
            info = self.get_info_from_element(element)
            pprint(info)
            self.all_vacancy.append(info)

    def get_total_page(self):
        html_string = self.get_html_string(params=self.start_params)
        soup = VacancyScrapper.get_dom(html_string)
        try:
            return int(soup.find_all('a', attrs={'data-qa': 'pager-page'})[-1].text)
        except IndexError as e:
            print('One page')
            return 1

    def run(self):
        if self.start_page_count:
            page = int(self.start_page_count)
        else:
            page = self.get_total_page()
        self.process_page(params=self.start_params)
        for page_number in range(1, page):
            print(f'page {page_number}')
            params = self.start_params
            params['page'] = page_number
            self.process_page(params=params)
            sleep(5)


if __name__ == "__main__":
    PARAMS['text'] = input('Job title: ')
    page_count = input('number of pages: ')
    scraper = VacancyScrapper(URL, PARAMS, HEADERS, page_count=page_count)
    scraper.run()
    scraper.save_vacancy_info()
