import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline


class ProductparserPipeline:
    def process_item(self, item, spider):
        # print("process item")
        # print()
        return item


class ProductparserImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item["img_urls"]:
            for img_url in item["img_urls"]:
                try:
                    yield scrapy.Request(img_url)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        print("ITEM_COMPLETED")
        if results:
            item["img_info"] = [i[1] for i in results if i[0]]
            del item["img_urls"]
        print(item)
        return item
