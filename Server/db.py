from pymongo import MongoClient
from config import MONGODB_CONN_STRING
from pymongo.errors import ConnectionFailure

try:
    client = MongoClient(MONGODB_CONN_STRING)
    client.admin.command('ismaster')
    print("MongoDB connection successful")
except ConnectionFailure as e:
    print(f"MongoDB connection failed: {e}")
    raise SystemExit("Terminating due to MongoDB connection failure")


db = client.Career_Sync

def insert_one(collection, entity):
    try:
        result = collection.insert_one(entity)
        if result.acknowledged:
            return entity
        else:
            raise ValueError("Insert operation not acknowledged")
    except Exception as e:
        print(f"Error during insert_one operation: {e}")
        raise ValueError("Failed to insert document") from e

def insert_many(collection, entities):
    try:
        result = collection.insert_many(entities)
        if result.acknowledged:
            return True
        else:
            raise ValueError("Insert operation not acknowledged")
    except Exception as e:
        print(f"Error during insert_many operation: {e}")
        raise ValueError("Failed to insert documents") from e