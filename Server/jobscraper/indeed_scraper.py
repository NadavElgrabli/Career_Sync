import os
import sys
import asyncio
from dotenv import find_dotenv, load_dotenv
from playwright.sync_api import sync_playwright, Locator
import re
import pymongo

class IndeedJobScraper:

    def __init__(self, **kwargs ):
        self.max_jobs = 5
        self.job = str(kwargs.get("job")).replace(' ', '+')
        self.location = str(kwargs.get('location', 'San Lorenzo')).title().replace(" ", "+")
        self.url = f"https://www.indeed.com/jobs?q={self.job}&l={self.location}&ts=1729499545404&from=searchOnHP&rq=1&rsIdx=1&fromage=last&vjk=8e448e208480d912"
        self.conn_to_mongo()
        
    def conn_to_mongo(self):
        load_dotenv(find_dotenv())
        mongodb_pwd = os.getenv('MONGODB_PWD')
        self.mongo_db = os.getenv('MONGODB_DB', 'Career_Sync')
        self.mongo_conn_string = f"mongodb+srv://nadavbarda:{mongodb_pwd}@cluster0.wmtsesk.mongodb.net/{self.mongo_db}?retryWrites=true&w=majority"
        self.mongo_collection = 'jobs'
        self.client = pymongo.MongoClient(self.mongo_conn_string)
        self.db = self.client[self.mongo_db]
        self.collection = self.db[self.mongo_collection]
        
    def fetch_page_content(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()

            page.goto(self.url)
            job_cards = page.locator("td.resultContent").all()
            prev_title = ""

            for count, job_card in enumerate(job_cards):
                if count >= self.max_jobs:
                    break
                job_card.click()
                job = page.locator("div.jobsearch-RightPane")
                job_dic = self.parse_job(job,prev_title)
                self.save_db(job_dic,prev_title)
                prev_title = job_dic.get('title','')
            browser.close()
            
            
    def save_db(self, job_dic, prev_title):
        if job_dic.get('title', '') == prev_title:
            return
        existing_item = self.collection.find_one({
            "title": job_dic.get("title"),
            "location": job_dic.get("location"),
            "job_type": job_dic.get("job_type"),
            'organization' : job_dic.get("organization"),
        })
        if existing_item:
            return
        self.collection.insert_one(job_dic)

        
    def remove_char(self,string :str,char_to_remove:str, count = 1):
        char_to_remove = "-"
        result = string.replace(char_to_remove, "", count)
        result = result.lstrip()
        return result
        
    def get_job_type(self, job: Locator) -> str:
        job_type_element = job.locator("div#salaryInfoAndJobType span.css-k5flys")
        job_type = None
        if job_type_element.count() > 0:  
            job_type = job_type_element.text_content()
            job_type = self.remove_char(job_type,'-')
        else :
            job_type = "Full-time"
        return job_type
    
    def get_job_location(self, job: Locator) -> str:
        
        location_element = job.locator('[data-testid="inlineHeader-companyLocation"] div')
        if location_element.count() > 0:
            location = location_element.text_content()
            return location.strip()
        return ""
    
    def get_job_url(self, job: Locator) -> str:
        btn = job.locator("div#applyButtonLinkContainer button")
        url = btn.get_attribute('href')
        return url
    
    def get_job_description(self, job: Locator) -> str:
        """Retrieves the job description without HTML tags."""
        description_element = job.locator("div#jobDescriptionText")
        if description_element.count() > 0:
            html_content = description_element.inner_html()
            text_content = re.sub('<[^<]+?>', '', html_content)
            return text_content.strip().lower()
        return ""
    
    def get_job_organization(self, job):
        organization_element = job.locator('[data-testid="inlineHeader-companyName"]')
        return organization_element.inner_text()

    
    def parse_job(self,job: Locator, last_job_title: str) :
    
        title = job.locator("h2.jobsearch-JobInfoHeader-title").text_content().split(" - ")[0]
        if title == last_job_title :
            self.max_jobs += 1
            return {'title' : last_job_title} 
        
        job_type = self.get_job_type(job)
        location = self.get_job_location(job)
        url = self.get_job_url(job)
        description = self.get_job_description(job)
        organization = self.get_job_organization(job)
        job_dic = {
            'title' : title,
            'job_type' : job_type,
            'location' : location,
            'url' : url,
            'description' : description,
            'organization':organization
        }
        
        return job_dic

if __name__ == "__main__":
    scraper = IndeedJobScraper(job="full stack", location="remote", max_jobs=5, headless=False)
    scraper.fetch_page_content()

