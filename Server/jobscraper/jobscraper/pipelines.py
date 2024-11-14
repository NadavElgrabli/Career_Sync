import re
from dotenv import find_dotenv, load_dotenv
from bs4 import BeautifulSoup
from jobscraper.jobscraper.items import JobscraperItem
import os
import pymongo
import os


class JobscraperPipeline:
    def process_item(self, item : JobscraperItem, spider):
        
        description = self.description_html_2_txt(item['description']).lower()
        item['description'] = description
        description_lower = description.lower()
        item['job_preference'] = self.extract_work_preference(description_lower)
        item['job_type'] = self.extract_job_type(description_lower)
        return item
    
    
    def extract_job_type(self, description):
        if re.search(r'\b(full[-\s]?time|permanent)\b', description):
            return 'Full-time'
        elif re.search(r'\b(part[-\s]?time)\b', description):
            return 'Part-time'
        elif re.search(r'\b(contract|contractor|freelance|temp|temporary)\b', description):
            return 'Contract'
        elif re.search(r'\b(intern|internship)\b', description):
            return 'Internship'
        elif re.search(r'\b(volunteer)\b', description):
            return 'Volunteer'
        else:
            return 'Full-time'
        
    def extract_work_preference(self,description):
    
        if re.search(r'\b(remote|work from home|telecommute|fully remote|anywhere)\b', description):
            return 'Remote'
        elif re.search(r'\b(on-site|on site|office-based|in-office|in office)\b', description):
            return 'Onsite'
        elif re.search(r'\b(hybrid|flexible work|partially remote)\b', description):
            return 'Hybrid'
        else:
            return 'Onsite'


    def description_html_2_txt(self,html_content):
        soup = BeautifulSoup(html_content, 'lxml')
        return soup.get_text()



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
        if existing_item or (not item.get("url")):
            return item
        self.collection.insert_one(dict(item))
        return item
