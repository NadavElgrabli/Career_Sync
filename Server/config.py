import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

MONGODB_PWD = os.environ.get("MONGODB_PWD")
MONGODB_CONN_STRING = f"mongodb+srv://nadavbarda:{MONGODB_PWD}@cluster0.wmtsesk.mongodb.net/?retryWrites=true&w=majority"
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")

