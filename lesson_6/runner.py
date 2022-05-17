from jobparser.spiders.hhru import HhruSpider
from jobparser.spiders.sjru import SjruSpider
from jobparser import settings

from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings


if __name__ == "__main__":
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)

    query = input()

    pkwargs = {
        "query": query,
    }
    process.crawl(HhruSpider, **pkwargs)
    # process.crawl(SjruSpider, **pkwargs)

    process.start()
