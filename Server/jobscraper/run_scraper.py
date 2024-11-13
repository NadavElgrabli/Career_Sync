from jobscraper.jobscraper.spiders.jobisjob import JobisjobSpider
from jobscraper.jobscraper.spiders.monsterspider import MonsterspiderSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from jobscraper.indeed_scraper import IndeedJobScraper
import os
from multiprocessing import Process

class Scraper:
    def __init__(self, **kwargs):
        settings_file_path = 'jobscraper.jobscraper.settings'
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
        self.spiders = [JobisjobSpider, MonsterspiderSpider] 
        self.job_preference = kwargs

    def run_spider(self, spider):
        process = CrawlerProcess(get_project_settings())
        process.crawl(spider, **self.job_preference)
        process.start()

    def run_spiders(self):
        # Run Indeed scraper in a separate process
        indeed_process = Process(target=self.run_indeed_scraper)
        indeed_process.start()

        spider_processes = []
        for spider in self.spiders:
            p = Process(target=self.run_spider, args=(spider,))
            p.start()
            spider_processes.append(p)

        indeed_process.join()
        for p in spider_processes:
            p.join()

    def run_indeed_scraper(self):
        indeed_scraper = IndeedJobScraper(**self.job_preference)
        indeed_scraper.fetch_page_content()
