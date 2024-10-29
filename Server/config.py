import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


MONGODB_PWD = os.environ.get("MONGODB_PWD")
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")

if not MONGODB_PWD:
    raise ValueError("MONGODB_PWD environment variable is missing")
if not JWT_SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY environment variable is missing")


MONGODB_CONN_STRING = f"mongodb+srv://nadavbarda:{MONGODB_PWD}@cluster0.wmtsesk.mongodb.net/Career_Sync?retryWrites=true&w=majority"


