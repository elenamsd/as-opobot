from pymongo import MongoClient
from config import MONGO_URI, DB_NAME

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

def get_collection_data(collection_name):
    collection = db[collection_name]
    return list(collection.find({}, {"_id": 0}))