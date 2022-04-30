import json
import re
from pprint import pprint

from lesson_2.vacanсies_scrapper import VacancyScrapper

URL = 'https://www.superjob.ru/vacancy/search/'
PARAMS = {
    'keywords': '',
    'page': 1,
}
HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10"}


class SuperJobVacancyScrapper(VacancyScrapper):

    def get_vacancy_name(self, element):
        name = element.findChild('div', attrs={'class': '_1M4pN _1O2dw _6kSO2 fmJDo'})
        if name:
            return name.span.text

    def get_vacancy_pay(self, element):
        zp = element.findChild('div', attrs={'class': '_1M4pN _1O2dw _6kSO2 fmJDo'})
        if zp:
            return zp.findChild('span', attrs={'class': '_4Gt5t _2jvwc f-test-text-company-item-salary'}).text
        return None

    @staticmethod
    def compile_str(str_zp):
        return re.compile(r'\d+\xa0\d+|\d+').findall(str_zp)[0].encode("ascii", "ignore").decode()

    @classmethod
    def compile_payment(cls, str_zp):
        payments = {}
        if str_zp:
            currency = str_zp[str_zp.rfind(' ') + 1:]
            if str_zp.startswith('от'):
                payments["min"] = int(cls.compile_str(str_zp))
                payments["max"] = None
                payments['currency'] = currency
                return payments
            elif str_zp.startswith('до'):
                payments["min"] = None
                payments["max"] = int(cls.compile_str(str_zp))
                payments['currency'] = currency
                return payments
            elif str_zp.startswith('По'):
                return 'По договорённости'
            elif re.search(r'\d+', str_zp).string and not ('—' in str_zp):
                payments["min"] = None
                payments["max"] = int(cls.compile_str(str_zp))
                payments['currency'] = currency
                return payments
            else:
                range_zp = re.split(r'—', str_zp)
                payments["min"] = int(cls.compile_str(range_zp[0]))
                payments["max"] = int(cls.compile_str(range_zp[1]))
                payments['currency'] = currency
                return payments
        else:
            return None

    def get_vacancy_requirements(self, element):
        span = element.find('span', attrs={'class': '_1AFgi _4uUzb _1TcZY mO3i1 dAWx1 Zruy6'})
        if span:
            return span.text
        return None

    def get_vacancy_url(self, element):
        span = element.find('span', attrs={'class': '-gENC _1TcZY Bbtm8'})
        if span:
            return 'https://www.superjob.ru' + span.a['href']
        return None

    def get_vacancy_employer(self, element):
        employer_element = element.findChild('span', attrs={'class': '_3nMqD f-test-text-vacancy-item-company-name '
                                                                     '_4uUzb _1TcZY mO3i1 dAWx1 Zruy6'})
        if employer_element:
            return employer_element.text
        return None

    def get_info_from_element(self, element, site='www.superjob.ru'):
        info = {}
        try:
            info['vacancy_payments'] = self.compile_payment(self.get_vacancy_pay(element))
            info['vacancy_name'] = self.get_vacancy_name(element)
            info['requirements'] = self.get_vacancy_requirements(element)
            info['vacancy_url'] = self.get_vacancy_url(element)
            info['employer'] = self.get_vacancy_employer(element)
            info['vacancy_site'] = site
        except ValueError as e:
            print(e)
        return info

    def process_page(self, params):
        html_string = self.get_html_string(params)
        if html_string is None:
            print("There was an error")
            return

        soup = VacancyScrapper.get_dom(html_string)
        vacancy_elements = soup.find_all('div', attrs={'class': 'f-test-search-result-item'})

        for element in vacancy_elements:
            info = self.get_info_from_element(element)
            if info['employer'] and info['vacancy_name']:
                pprint(info)
                self.all_vacancy.append(info)

    def save_vacancy_info(self):
        with open(PARAMS['keywords'], 'w', encoding='utf-8') as f:
            json.dump(self.all_vacancy, f, indent=4)


if __name__ == "__main__":
    PARAMS['keywords'] = input('Job title: ')
    page_count = input('number of pages: ')
    scraper = SuperJobVacancyScrapper(url=URL, params=PARAMS, headers=HEADERS, page_count=page_count)
    scraper.run()
    scraper.save_vacancy_info()
