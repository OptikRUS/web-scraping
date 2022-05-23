from bookparser.spiders.chitai import ChitaiSpider
from bookparser import settings

from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings


if __name__ == "__main__":
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)

    process.crawl(ChitaiSpider)

    process.start()
