import re
from dotenv import find_dotenv, load_dotenv
from bs4 import BeautifulSoup
from controller.job_score import calculate_total_score
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
        item['experience'] = self.extract_experience(description_lower)
        
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

    
    
    def extract_experience(self,description):
        matches = re.findall(r'(\d+)\+?\s+years? of experience', description)
        if matches:
            return int(matches[0])
        else:
            return None 
    
    def description_html_2_txt(self,html_content):
        soup = BeautifulSoup(html_content, 'lxml')
        return soup.get_text()



class MongoDBPipeline:
    def __init__(self, mongo_conn_string, mongo_db, mongo_job_collection,mongo_user_collection):
        self.mongo_conn_string = mongo_conn_string
        self.mongo_db = mongo_db
        self.mongo_job_collection = mongo_job_collection
        self.mongo_user_collection = mongo_user_collection
        

    @classmethod
    def from_crawler(cls, crawler):
        load_dotenv(find_dotenv())

        mongodb_pwd = os.getenv('MONGODB_PWD')
        mongodb_db = os.getenv('MONGODB_DB', 'Career_Sync')
        mongo_conn_string = f"mongodb+srv://nadavbarda:{mongodb_pwd}@cluster0.wmtsesk.mongodb.net/{mongodb_db}?retryWrites=true&w=majority"

        return cls(
            mongo_conn_string=mongo_conn_string,
            mongo_db=mongodb_db,
            mongo_job_collection= "jobs",
            mongo_user_collection= 'users'
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_conn_string)
        self.db = self.client[self.mongo_db]
        self.job_collection = self.db[self.mongo_job_collection]
        self.user_collection = self.db[self.mongo_user_collection]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item : JobscraperItem, spider):
        username = getattr(spider, 'username', None)
        self.kwargs = getattr(spider, 'kwargs', None)
        job_id = self.save_db(item)
        self.save_job_on_user(job_id,item,username)
    
    def save_db(self, job_dic):
        existing_item = self.job_collection.find_one({
            "title": job_dic.get("title"),
            "location": job_dic.get("location"),
            "organization": job_dic.get("organization"),
        })

        if existing_item:
            return str(existing_item["_id"])
        
        result = self.job_collection.insert_one(dict(job_dic))

        return str(result.inserted_id)

    
    def save_job_on_user(self, job_id,job_dic,username):
        user = self.user_collection.find_one({"username": username})
        if not user:
            raise ValueError("User not found")
        
        jobs = user.get("jobs", [])

        for job in jobs:
            if job.get("job_id") == job_id:
                return  
        
        candidate_profile = self.kwargs
        
        score = calculate_total_score(candidate_profile=candidate_profile, job_data=job_dic)
        
        job_data = {
            'score': score,
            'job_id': job_id,
            'applied': False,
        }
        
        jobs.append(job_data)
        
        self.user_collection.update_one(
            {"username": username},
            {"$push": {"jobs": job_data}}
        )