from pymongo import MongoClient
from config import MONGODB_CONN_STRING

client = MongoClient(MONGODB_CONN_STRING)
db = client.Career_Sync



from pymongo import MongoClient
from config import MONGODB_CONN_STRING

client = MongoClient(MONGODB_CONN_STRING)
db = client.Career_Sync

def insert_one(collection, entity):
    
    try:
        result = collection.insert_one(entity)
        if result.acknowledged:
            return entity
        else:
            raise ValueError("Insert operation not acknowledged")
    except Exception as e:
        raise ValueError("Failed to insert document")

def insert_many(collection, entities):
    try:
        result = collection.insert_many(entities)
        if result.acknowledged:
            return True
        else:
            raise ValueError("Insert operation not acknowledged")
    except Exception as e:
        raise ValueError("Failed to insert documents")
