from pymongo import MongoClient
from config import MONGODB_CONN_STRING

client = MongoClient(MONGODB_CONN_STRING)
db = client.Career_Sync


