import os
import time
from dotenv import find_dotenv, load_dotenv
from playwright.async_api import async_playwright, Locator
import re
import pymongo
from controller.job_score import calculate_total_score
import asyncio

class IndeedJobScraper:

    def __init__(self, **kwargs):
        self.max_jobs = kwargs.get('max_jobs', 5)
        self.headless = kwargs.get('headless', False)
        self.job = str(kwargs.get("job")).replace(' ', '+')
        self.location = str(kwargs.get('location', 'San Lorenzo')).title().replace(" ", "+")
        self.url = f"https://www.indeed.com/jobs?q={self.job}&l={self.location}&from=searchOnDesktopSerp"
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

    async def fetch_page_content(self):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=self.headless)
            page = await browser.new_page()

            await page.goto(self.url)
            page.wait_for_load_state("networkidle")
            job_cards = await page.locator("td.resultContent").all()
            prev_title = ""
            time.sleep(1)
            for count, job_card in enumerate(job_cards):
                if count >= self.max_jobs:
                    break

                await job_card.scroll_into_view_if_needed(timeout=5000)
                await job_card.click()
                job = page.locator("div.jobsearch-RightPane")
                try:
                    await job.wait_for(state='visible', timeout=2000)
                    await job.locator("h2.jobsearch-JobInfoHeader-title").wait_for(state='visible', timeout=5000)
                except Exception as e:
                    print(f"Failed to load job details for job card {count}: {e}")
                    break

                job_dic = await self.parse_job(job, prev_title)
                self.handle_job_save(job_dic, prev_title)
                prev_title = job_dic.get('title', '')

            await browser.close()

    async def parse_job(self, job: Locator, last_job_title: str):
        title_element = job.locator("h2.jobsearch-JobInfoHeader-title")
        title_text = await title_element.text_content()
        title = title_text.split(" - ")[0]
        if title == last_job_title:
            self.max_jobs += 1
            return {'title': last_job_title}

        job_type = await self.get_job_type(job)
        location = await self.get_job_location(job)
        url = await self.get_job_url(job)
        organization = await self.get_job_organization(job)
        description = await self.get_job_description(job)
        lower_description = description.lower()
        job_preference = self.extract_work_preference(lower_description)
        experience = self.extract_experience(lower_description)
        job_dic = {
            'title': title,
            'job_type': job_type,
            'location': location,
            'url': url,
            'description': description,
            'organization': organization,
            'job_preference': job_preference,
            'experience': experience
        }

        return job_dic

    async def get_job_type(self, job: Locator) -> str:
        job_type_element = job.locator("div#salaryInfoAndJobType span.css-k5flys")
        count = await job_type_element.count()
        if count > 0:
            job_type = await job_type_element.text_content()
            job_type = self.remove_char(job_type, '-')
        else:
            job_type = "Full-time"
        return job_type

    async def get_job_location(self, job: Locator) -> str:
        location_element = job.locator('[data-testid="inlineHeader-companyLocation"] div')
        count = await location_element.count()
        if count > 0:
            location = await location_element.text_content()
            return location.strip()
        return ""

    async def get_job_url(self, job: Locator) -> str:
        btn = job.locator("div#applyButtonLinkContainer button")
        url = await btn.get_attribute('href')
        return url

    async def get_job_description(self, job: Locator) -> str:
        description_element = job.locator("div#jobDescriptionText")
        count = await description_element.count()
        if count > 0:
            html_content = await description_element.inner_html()
            text_content = re.sub('<[^<]+?>', '', html_content)
            return text_content.strip()
        return ""

    async def get_job_organization(self, job: Locator) -> str:
        organization_element = job.locator('[data-testid="inlineHeader-companyName"]')
        organization_text = await organization_element.inner_text()
        return organization_text

    def extract_work_preference(self, description):
        if re.search(r'\b(remote|work from home|telecommute|fully remote|anywhere)\b', description):
            return 'Remote'
        elif re.search(r'\b(on-site|on site|office-based|in-office|in office)\b', description):
            return 'Onsite'
        elif re.search(r'\b(hybrid|flexible work|partially remote)\b', description):
            return 'Hybrid'
        else:
            return 'Onsite'

    def extract_degree_fields(self, description):
        pattern = r"(?:bachelor's|master's|phd|doctorate)?\s*(?:degree)?\s*(?:in|of)\s+([\w\s&\-,]+)"
        matches = re.findall(pattern, description)
        if matches:
            fields = [match.strip().strip('.').strip(',') for match in matches]
            return fields
        else:
            return []

    def extract_experience(self, description):
        matches = re.findall(r'(\d+)\+?\s+years? of experience', description)
        if matches:
            return int(matches[0])
        else:
            return None

    def remove_char(self, string: str, char_to_remove: str, count=1):
        char_to_remove = "-"
        result = string.replace(char_to_remove, "", count)
        result = result.lstrip()
        return result

    def handle_job_save(self, job_dic, prev_title):
        if job_dic.get('title', '') == prev_title:
            return None
        job_id = self.save_db(job_dic, prev_title)
        self.save_job_on_user(job_id, job_dic)

    def save_db(self, job_dic, prev_title):
        existing_item = self.job_collection.find_one({
            "title": job_dic.get("title"),
            "location": job_dic.get("location"),
            "organization": job_dic.get("organization"),
        })
        if existing_item:
            return str(existing_item["_id"])
        result = self.job_collection.insert_one(job_dic)
        return str(result.inserted_id)

    def save_job_on_user(self, job_id, job_dic):
        user = self.user_collection.find_one({"username": self.username})
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
            {"username": self.username},
            {"$push": {"jobs": job_data}}
        )

if __name__ == "__main__":
    scraper = IndeedJobScraper(job="full stack", location="remote", max_jobs=5, headless=False)
    asyncio.run(scraper.fetch_page_content())
