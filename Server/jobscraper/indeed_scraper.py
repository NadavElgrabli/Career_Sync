import os
from dotenv import find_dotenv, load_dotenv
from playwright.sync_api import sync_playwright, Locator
import re
import pymongo
from controller.job_score import calculate_total_score

class IndeedJobScraper:

    def __init__(self, **kwargs ):
        self.max_jobs = 5
        self.job = str(kwargs.get("job")).replace(' ', '+')
        self.location = str(kwargs.get('location', 'San Lorenzo')).title().replace(" ", "+")
        self.url = f"https://www.indeed.com/jobs?q={self.job}&l={self.location}&ts=1729499545404&from=searchOnHP&rq=1&rsIdx=1&fromage=last&vjk=8e448e208480d912"
        self.username = kwargs.get("username")
        self.kwargs = kwargs
        self.conn_to_mongo()
    
    def conn_to_mongo(self):
        load_dotenv(find_dotenv())
        mongodb_pwd = os.getenv('MONGODB_PWD')
        self.mongo_db = os.getenv('MONGODB_DB', 'Career_Sync')
        self.mongo_conn_string = f"mongodb+srv://nadavbarda:{mongodb_pwd}@cluster0.wmtsesk.mongodb.net/{self.mongo_db}?retryWrites=true&w=majority"
        self.mongo_job_collection = 'jobs'
        self.client = pymongo.MongoClient(self.mongo_conn_string)
        self.db = self.client[self.mongo_db]
        self.job_collection = self.db[self.mongo_job_collection]
        self.user_collection = self.db['users']
        
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
                self.handle_job_save(job_dic,prev_title)
                prev_title = job_dic.get('title','')
            browser.close()
          
          
    def save_job_on_user(self, job_id,job_dic):
        user = self.user_collection.find_one({"username": self.username})
        if not user:
            raise ValueError("User not found")
        
        jobs = user.get("jobs", [])

        for job in jobs:
            if job.get("job_id") == job_id:
                return  
        
        candidate_profile = self.kwargs
        # Calculate the score (implement your logic here)
        score = calculate_total_score(candidate_profile=candidate_profile, job_data=job_dic)
        
        job_data = {
            'score': score,
            'job_id': job_id,
            'applied': False,
        }
        
        jobs.append(job_data)
        
        self.user_collection.update_one(
            {"username": self.username},
            {"$push": {"jobs": job_data}}
        )

    
    def handle_job_save(self,job_dic, prev_title):
        job_id = self.save_db(job_dic,prev_title)
        self.save_job_on_user(job_id,job_dic)
        
        
            
    def save_db(self, job_dic, prev_title):
        if job_dic.get('title', '') == prev_title:
            return None

        existing_item = self.job_collection.find_one({
            "title": job_dic.get("title"),
            "location": job_dic.get("location"),
            "organization": job_dic.get("organization"),
        })

        if existing_item:
            return str(existing_item["_id"])
        
        result = self.job_collection.insert_one(job_dic)

        return str(result.inserted_id)


        
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
            return text_content.strip()
        return ""
    
    def get_job_organization(self, job):
        organization_element = job.locator('[data-testid="inlineHeader-companyName"]')
        return organization_element.inner_text()

    def extract_work_preference(self,description):
    
        if re.search(r'\b(remote|work from home|telecommute|fully remote|anywhere)\b', description):
            return 'Remote'
        elif re.search(r'\b(on-site|on site|office-based|in-office|in office)\b', description):
            return 'Onsite'
        elif re.search(r'\b(hybrid|flexible work|partially remote)\b', description):
            return 'Hybrid'
        else:
            return 'Onsite'

    def extract_degree_fields(self,description):
        
        pattern = r"(?:bachelor's|master's|phd|doctorate)?\s*(?:degree)?\s*(?:in|of)\s+([\w\s&\-,]+)"
        matches = re.findall(pattern, description)
        if matches:
            fields = [match.strip().strip('.').strip(',') for match in matches]
            return fields  
        else:
            return []
        
        
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
        job_preference = self.extract_work_preference(description.lower())
        job_dic = {
            'title' : title,
            'job_type' : job_type,
            'location' : location,
            'url' : url,
            'description' : description,
            'organization':organization,
            'job_preference' : job_preference
        }
        
        return job_dic

if __name__ == "__main__":
    scraper = IndeedJobScraper(job="full stack", location="remote", max_jobs=5, headless=False)
    scraper.fetch_page_content()

