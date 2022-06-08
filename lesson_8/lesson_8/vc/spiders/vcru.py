import scrapy
from scrapy.http import TextResponse, FormRequest


class VcruSpider(scrapy.Spider):
    name = "vcru"
    allowed_domains = ["vc.ru"]
    start_urls = ["https://vc.ru/"]
    login_url = "https://vc.ru/auth/simple/login"
    interesting_url = "https://vc.ru/u/980897-vasiliy-cherepanov"
    subscribers = interesting_url + '/details/subscribers'
    # max_posts_page_number = 5
    # template_url = (
    #     "https://vc.ru/marketing/more?"
    #     "last_id=%s&last_sorting_value=%s"
    #     "&page=%s&exclude_ids=[]&mode=raw"
    # )

    def __init__(self, login, password):
        super().__init__()
        self.login = login
        self.password = password

    def parse(self, response: TextResponse, **kwargs):
        print("PARSE")
        print(response.url)
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
        yield response.follow(self.subscribers, callback=self.parse_subscribers)

    def parse_subscribers(self, response: TextResponse):
        print("SUBSCRIBERS")
        subscribers = response.xpath("//a[@class='v-list-subsites-item__main']")
        print()




