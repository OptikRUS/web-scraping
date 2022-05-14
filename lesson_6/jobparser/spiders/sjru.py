import scrapy
from scrapy.http import TextResponse
from ..items import JobparserItem

TEMPLATE_URL = 'https://rostovskaya-oblast.superjob.ru/vacancy/search/?keywords='


class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['http://superjob.ru/']
    max_page_number = 5

    def __init__(self, query, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [
            TEMPLATE_URL + query
        ]

    def parse_item(self, response: TextResponse):
        title_xpath = '//h1//text()'
        salary_xpath = '//span[@class="_2eYAG -gENC _1TcZY dAWx1"]/text()'
        title = response.xpath(title_xpath).getall()
        salary = response.xpath(salary_xpath).getall()
        item = JobparserItem()
        item['title'] = ' '.join(title)
        item['salary'] = salary
        item['url'] = response.url
        yield item

    def parse(self, response: TextResponse, page_number: int = 1, **kwargs):
        items = response.xpath('//span[contains(@class, "-gENC _1TcZY Bbtm8")]/a')
        for item in items:
            url = item.xpath("./@href").get()
            yield response.follow(url, callback=self.parse_item)
        next_url = response.xpath('//a[contains(@rel, "next")]').get()
        if next_url and page_number < self.max_page_number:
            new_kwargs = {"page_number": page_number + 1}
            yield response.follow(next_url, callback=self.parse, cb_kwargs=new_kwargs)
