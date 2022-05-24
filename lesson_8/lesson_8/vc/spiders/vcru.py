import scrapy
from scrapy import FormRequest
from scrapy.http import TextResponse


class VcruSpider(scrapy.Spider):
    name = "vcru"
    allowed_domains = ["vc.ru"]
    users = ["https://vc.ru/u/14066-andrey-frolov", "https://vc.ru/u/28953-alina-tolmacheva"]
    start_urls = [i + '/details/subscribers' for i in users]
    login_url = "https://vc.ru/auth/simple/login"
    max_page_number = 5

    def parse(self, response: TextResponse, page_number: int = 1, **kwargs):
        subscribers = response.xpath('//a[@class="v-list-subsites-item__main"]')
        print()
        for item in subscribers:
            url = item.xpath("./@href").get()
            yield response.follow(url, callback=self.parse_user)

    def parse_user(self, response: TextResponse):
        name_xpath = '//a[@class="v-header-title__item v-header-title__name"]/text()'
        img_xpath = '//div[@class="v-header-avatar v-header-avatar--with-zoom"]/@style'

        print()



