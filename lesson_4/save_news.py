from pymongo import MongoClient

MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DB = "news"
MONGO_COLLECTION = "all_news"


def save_news_item(info):
    with MongoClient(MONGO_HOST, MONGO_PORT) as client:
        db = client[MONGO_DB]
        collection =db[MONGO_COLLECTION]
        collection.update_one({"name": {"$eq": info['name']}}, {"$set": info}, upsert=True)
