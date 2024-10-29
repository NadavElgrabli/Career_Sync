
from dotenv import find_dotenv, load_dotenv
from itemadapter import ItemAdapter
from bs4 import BeautifulSoup
from jobscraper.items import JobscraperItem
import os
import pymongo
import os
from jobscraper.items import JobscraperItem



def description_html_2_txt(html_content):
    soup = BeautifulSoup(html_content, 'lxml')
    return soup.get_text()


class JobscraperPipeline:
    def process_item(self, item : JobscraperItem, spider):
        item['description'] = description_html_2_txt(item['description'])
        return item




MAX_LEN_DESCRIPTION = 100


class MongoDBPipeline:
    def __init__(self, mongo_conn_string, mongo_db, mongo_collection):
        self.mongo_conn_string = mongo_conn_string
        self.mongo_db = mongo_db
        self.mongo_collection = mongo_collection

    @classmethod
    def from_crawler(cls, crawler):
        load_dotenv(find_dotenv())

        mongodb_pwd = os.getenv('MONGODB_PWD')
        mongodb_db = os.getenv('MONGODB_DB', 'Career_Sync')
        mongo_conn_string = f"mongodb+srv://nadavbarda:{mongodb_pwd}@cluster0.wmtsesk.mongodb.net/{mongodb_db}?retryWrites=true&w=majority"

        return cls(
            mongo_conn_string=mongo_conn_string,
            mongo_db=mongodb_db,
            mongo_collection= "jobs"
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_conn_string)
        self.db = self.client[self.mongo_db]
        self.collection = self.db[self.mongo_collection]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item : JobscraperItem, spider):
        existing_item = self.collection.find_one({"url": item.get("url")})
        if existing_item:
            return item
        item['description'] = item['description'][0:MAX_LEN_DESCRIPTION]
        self.collection.insert_one(dict(item))
        return item
