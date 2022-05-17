import scrapy
from scrapy.http import TextResponse
from ..items import ProductparserItem


class LeruaSpider(scrapy.Spider):
    name = 'lerua'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['https://leroymerlin.ru/catalogue/osveshchenie/']
    max_page_number = 30

    def parse_item(self, response: TextResponse):
        print('parse item')
        title_xpath = '//h1[@slot="title"]//text()'
        price_xpath = '//span[@slot="price"]//text()'
        article_xpath = '//span[@slot="article"]//text()'
        img_urls_xpath = '//img[@slot="thumbs"]//'
        params_xpath = '//div[@class="def-list__group"]'
        title = response.xpath(title_xpath).getall()
        price = response.xpath(price_xpath).getall()
        article = response.xpath(article_xpath).getall()
        img_urls = response.xpath(img_urls_xpath).getall()
        params = response.xpath(params_xpath).getall()
        item = ProductparserItem()
        item['title'] = title
        item['price'] = int(price)
        item['article'] = int(article)
        item['url'] = response.url
        item['img_urls'] = img_urls
        item['params'] = params
        print()
        yield item

    def parse(self, response: TextResponse, page_number: int = 1, **kwargs):
        items = response.xpath('//a[@class="bex6mjh_plp b1f5t594_plp iypgduq_plp nf842wf_plp"]')
        for item in items:
            url = item.xpath("./@href").get()
            yield response.follow(url, callback=self.parse_item)
        next_url = response.xpath('//a[@data-qa-pagination-item="right"]/@href').get()
        if next_url and page_number < self.max_page_number:
            new_kwargs = {"page_number": page_number + 1}
            yield response.follow(next_url, callback=self.parse, cb_kwargs=new_kwargs)
