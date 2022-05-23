import scrapy
from scrapy.http import TextResponse
from scrapy.loader import ItemLoader

from ..items import BookparserItem


class ChitaiSpider(scrapy.Spider):
    name = 'chitai'
    allowed_domains = ['chitai-gorod.ru']
    start_urls = ['https://www.chitai-gorod.ru/catalog/books/khudozhestvennaya_literatura-9657/']
    max_page_number = 30

    def parse(self, response: TextResponse, page_number: int = 1, **kwargs):
        items = response.xpath('//a[@class="product-card__img js-analytic-productlink"]')
        for item in items:
            url = item.xpath("./@href").get()
            yield response.follow(url, callback=self.parse_item)
        next_url = response.xpath('//a[@id="navigation_1_next_page"]//@href').get()
        if next_url and page_number < self.max_page_number:
            new_kwargs = {"page_number": page_number + 1}
            yield response.follow(next_url, callback=self.parse, cb_kwargs=new_kwargs)

    def parse_item(self, response: TextResponse):
        title_xpath = '//h1[@itemprop ="name"]//text()'
        price_xpath = '//div[@class="price"]//text()'
        img_urls_xpath = '//meta[@itemprop="image"]/@content'
        annotation_xpath = '//div[@itemprop="description"]/text()'
        rate_xpath = '//span[@class="js__rating_count"]/text()'
        author_xpath = '//a[@class="link product__author"]/text()'
        params_xpath = '//div[@class="product-prop"]/div/text()[last()]'

        params_keys_xpath = '//div[@class="product-prop"]/div[@class="product-prop__title"]/text()'
        params_values_xpath = '//div[@class="product-prop"]/div[@class="product-prop__value"]'

        title = response.xpath(title_xpath).get()
        rate = response.xpath(rate_xpath).get()
        price = response.xpath(price_xpath).getall()
        annotation = response.xpath(annotation_xpath).get()
        author = response.xpath(author_xpath).get()

        loader = ItemLoader(item=BookparserItem(), response=response)

        loader.add_value("url", response.url)
        loader.add_value("title", title)
        loader.add_value("author", author)
        loader.add_value("rate", rate)
        loader.add_value("annotation", annotation)
        loader.add_value("price", price)
        loader.add_xpath("img_urls", img_urls_xpath)
        loader.add_xpath("params", params_xpath)

        yield loader.load_item()
