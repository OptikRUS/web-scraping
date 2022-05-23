import scrapy
from scrapy.http import TextResponse
from scrapy.http import Request
from scrapy.loader import ItemLoader
from selenium import webdriver

from ..items import ProductparserItem

DRIVER_PATH = "./selenium_drivers/chromedriver"


class LeruaSpider(scrapy.Spider):
    name = 'lerua'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['https://leroymerlin.ru/catalogue/osveshchenie/']
    max_page_number = 30

    # def start_requests(self):
    #     options = webdriver.ChromeOptions()
    #     driver = webdriver.Chrome(DRIVER_PATH, options=options)
    #
    #     driver.get('https://leroymerlin.ru/__qrator/qauth_utm_v2.js')
    #     cookies = driver.get_cookies()[0]
    #     print(cookies)
    #     yield Request(self.start_urls[0], cookies=cookies)
    #
    #     for url in self.start_urls:
    #         yield Request(url, callback=self.parse_item, cookies=cookies)

    def parse_item(self, response: TextResponse):
        print('parse item')
        title_xpath = '//h1[@slot="title"]//text()'
        price_xpath = '//span[@slot="price"]//text()'
        article_xpath = '//span[@slot="article"]//text()'
        img_urls_xpath = '//img[@slot="thumbs"]//'
        params_xpath = '//div[@class="def-list__group"]'

        title = response.xpath(title_xpath).get()
        price = response.xpath(price_xpath).getall()
        article = response.xpath(article_xpath).getall()
        img_urls = response.xpath(img_urls_xpath).getall()
        params = response.xpath(params_xpath).getall()

        loader = ItemLoader(item=ProductparserItem(), response=response)

        loader.add_value("url", response.url)
        loader.add_value("title", title)
        loader.add_value("price", price)
        loader.add_value("article", article)
        loader.add_xpath("img_urls", img_urls)
        loader.add_xpath("params", params)

        print()
        yield loader.load_item()

    def parse_search(self, response: TextResponse, page_number: int = 1, **kwargs):
        items = response.xpath('//a[@class="bex6mjh_plp b1f5t594_plp iypgduq_plp nf842wf_plp"]')
        for item in items:
            url = item.xpath("./@href").get()
            yield response.follow(url, callback=self.parse_item)
        next_url = response.xpath('//a[@data-qa-pagination-item="right"]/@href').get()
        if next_url and page_number < self.max_page_number:
            new_kwargs = {"page_number": page_number + 1}
            yield response.follow(next_url, callback=self.parse_search, cb_kwargs=new_kwargs)
