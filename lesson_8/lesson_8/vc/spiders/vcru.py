import scrapy
from scrapy.http import TextResponse, FormRequest
from ..items import VcItem


class VcruSpider(scrapy.Spider):
    name = "vcru"
    allowed_domains = ["vc.ru"]
    start_urls = ["https://vc.ru/"]
    login_url = "https://vc.ru/auth/simple/login"
    users_id = ['980897', '1023408']
    subscribers = "https://vc.ru/subsite/subscribers/"
    subscriptions = "https://vc.ru/subsite/subscriptions/"

    def __init__(self, login, password):
        super().__init__()
        self.login = login
        self.password = password

    def parse(self, response: TextResponse, **kwargs):
        print("PARSE")
        version = response.xpath("//link[@rel='stylesheet'" " and contains(@href, 'vc-')]/@href").get()
        version = version.split("/")[-1].split(".")[1]
        print()
        yield FormRequest(
            self.login_url,
            formdata={
                "values[login]": self.login,
                "values[password]": self.password,
                "mode": "raw",
            },
            headers={
                "origin": response.url,
                "referer": response.url,
                "x-js-version": version,
                "x-this-is-csrf": "THIS IS SPARTA!",
            },
            callback=self.parse_login,
            method="POST",
        )

    def parse_login(self, response: TextResponse):
        print("PARSE_LOGIN")
        print()
        data = response.json()
        if data["rc"] != 200:
            raise ValueError(f"Something went wrong with login: {data['rm']}")

        for user_id in self.users_id:
            yield response.follow(self.subscribers + user_id, callback=self.parse_subscribers)

    def parse_subscribers(self, response: TextResponse):
        print("SUBSCRIBERS")
        subscribers = response.json()['data']['items']
        print()
        for subscriber in subscribers:
            item = VcItem()
            item['user'] = response.url.split('/')[-1]
            item['user_id'] = subscriber['id']
            item['name'] = subscriber['label']
            item['url'] = subscriber['url']
            item['img_url'] = subscriber['image']
            yield item
            print()

