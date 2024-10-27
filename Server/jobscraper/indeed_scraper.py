from playwright.sync_api import sync_playwright, Locator

url = "https://www.indeed.com/jobs?q=full+stack&l=remote&ts=1729499545404&from=searchOnHP&rq=1&rsIdx=1&fromage=last&vjk=8e448e208480d912"


class IndeedJobScraper:

    def __init__(self, url, max_jobs=5, headless=False):
        self.url = url
        self.max_jobs = max_jobs
        self.headless = headless

    def fetch_page_content(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()

            page.goto(url)
            job_cards = page.locator("td.resultContent").all()
            prev_title = ""

            for count, job_card in enumerate(job_cards):
                if count >= self.max_jobs:
                    break
                job_card.click()
                job = page.locator("div.jobsearch-RightPane")
                prev_title = self.parse_job(job,prev_title)
                

            browser.close()


    def parse_job(self,job: Locator, last_job_title: str) -> str :
    
        title = job.locator("h2.jobsearch-JobInfoHeader-title").text_content().split(" - ")[0]
        if title == last_job_title :
            self.max_jobs += 1
            return last_job_title
        job_type_element = job.locator("div#salaryInfoAndJobType")
        job_type = None
        if job_type_element.count() > 0:  
            job_type = job_type_element.text_content()

        location_element = job.locator('[data-testid="inlineHeader-companyLocation"] div')
        location = None
        if location_element.count() > 0:
            location = location_element.text_content()
        
        btn = job.locator("div#applyButtonLinkContainer button")
        url = btn.get_attribute('href')

        if location:
            print("**************")
            print(f"Title: {title}")
            print(f"Job Type: {job_type}")
            print(f"Location: {location}")
            print(f'url : {url}')
            print("**************")
        
        return title

if __name__ == "__main__":
    url = "https://www.indeed.com/jobs?q=full+stack&l=remote&ts=1729499545404&from=searchOnHP&rq=1&rsIdx=1&fromage=last&vjk=8e448e208480d912"
    scraper = IndeedJobScraper(url=url, max_jobs=5, headless=False)
    scraper.fetch_page_content()
