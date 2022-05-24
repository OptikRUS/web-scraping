import scrapy


class VcruSpider(scrapy.Spider):
    name = 'vcru'
    allowed_domains = ['vc.ru']
    start_urls = ['http://vc.ru/']

    def parse(self, response):
        pass
