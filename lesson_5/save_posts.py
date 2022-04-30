from pymongo import MongoClient

MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DB = "posts"
MONGO_COLLECTION = "vk"


def save_posts(info):
    with MongoClient(MONGO_HOST, MONGO_PORT) as client:
        db = client[MONGO_DB]
        collection =db[MONGO_COLLECTION]
        collection.update_one({"text": {"$eq": info['text']}}, {"$set": info}, upsert=True)
