from pprint import pprint
from datetime import datetime
import requests

from lxml.html import fromstring

from lesson_4.save_news import save_news_item

URL = 'https://yandex.ru/news'
# HEADERS = {
#     "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
#                   "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
# }

ALL_TOP_NEWS_ITEMS = '(//div[contains(@class, "mg-grid__col mg-grid__col_xs_6")] | ' \
                     '//div[contains(@class, "mg-grid__col mg-grid__col_xs_4")])'

response = requests.get(URL)
dom = fromstring(response.text)

news_items = dom.xpath(ALL_TOP_NEWS_ITEMS)

for item in news_items:
    info = {}
    teg_a = item.xpath('.//h2[contains(@class, mg-mg-card__title)]/a')
    footer = item.xpath('.//div[contains(@class, "mg-card-source mg-card__source mg-card__source_dot")]')
    if teg_a and footer:
        full_url = teg_a[0].xpath('./@href')[0]
        info['url'] = full_url[:full_url.rfind('?')]
        info['name'] = teg_a[0].xpath('./text()')[0]
        date = footer[0].xpath('./span[contains(@class, "mg-card-source__time")]/text()')[0]
        # date_format = datetime.strptime(date, '%H:%M')
        info['date'] = date
        info['source'] = footer[0].xpath('.//a[contains(@class, "mg-card__source-link")]/text()')[0]

        pprint(info)
        save_news_item(info)

print()