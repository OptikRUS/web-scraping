from pprint import pprint
from datetime import datetime
import requests

from lxml.html import fromstring


URL = 'https://lenta.ru/'
HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    # "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "Connection": "keep-alive",
    "DNT": "1",
    "Host": "lenta.ru",
    "Referer": "https://lenta.ru/",
    "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "macOS",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
}
ALL_TOP_NEWS_ITEMS = '//a[contains(@class, "card-mini")]'

response = requests.get(URL, headers=HEADERS)
dom = fromstring(response.text)
# 'source': 'Lenta.ru'

print(response.text)
print(dom.xpath('//div'))

print()