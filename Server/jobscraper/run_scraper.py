from jobscraper.jobscraper.spiders.jobisjob import JobisjobSpider
from jobscraper.jobscraper.spiders.monsterspider import MonsterspiderSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from jobscraper.indeed_scraper import IndeedJobScraper
import os


class Scraper:
    def __init__(self,**kwargs):
        settings_file_path = 'jobscraper.jobscraper.settings'
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
        self.process = CrawlerProcess(get_project_settings())
        self.spiders = [JobisjobSpider,MonsterspiderSpider] 
        self.job_preference = kwargs

    def run_spiders(self):
        indeed_scraper = IndeedJobScraper(**self.job_preference)
        indeed_scraper.fetch_page_content()
        for spider in self.spiders :
            self.process.crawl(spider,**self.job_preference)
        self.process.start()
        