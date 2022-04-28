from pprint import pprint
from datetime import datetime
import requests

from lxml.html import fromstring


def get_info_from_url(url):
    info = {}
    dom = fromstring(requests.get(url, headers=HEADERS).text)
    item = dom.xpath('//div[contains(@class, "article js-article js-module")]')[0]
    info['source'] = item.xpath('//span[@class="note"]//span[@class="link__text"]/text()')[0]
    info['name'] = item.xpath('//h1[contains(@class, "hdr__inner")]/text()')[0]
    date = item.xpath('//span[@datetime]')[0].xpath('@datetime')[0]
    date_format = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z')
    info['date'] = date_format
    info['url'] = url

    return info


URL = 'https://news.mail.ru/'
HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10"}
ALL_TOP_NEWS_ITEMS = '//a[contains(@class, "js-topnews__item")]'

response = requests.get(URL, headers=HEADERS)
dom = fromstring(response.text)

news_links = [i.xpath('@href')[0] for i in dom.xpath(ALL_TOP_NEWS_ITEMS)]

for link in news_links:
    news_info = get_info_from_url(link)
    pprint(news_info)
