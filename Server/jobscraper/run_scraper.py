import os
import asyncio
from multiprocessing import Process
from jobscraper.jobscraper.spiders.jobisjob import JobisjobSpider
from jobscraper.jobscraper.spiders.monsterspider import MonsterspiderSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from jobscraper.indeed_scraper import IndeedJobScraper

class Scraper:
    def __init__(self, **kwargs):
        settings_file_path = 'jobscraper.jobscraper.settings'
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
        self.spiders = [JobisjobSpider, MonsterspiderSpider]
        self.job_preference = kwargs
        self.timeout = 30
        

    def run_spider(self, spider):
        process = CrawlerProcess(get_project_settings())
        process.crawl(spider, **self.job_preference)
        process.start()

    def run_spiders(self):
        indeed_process = Process(target=self.run_indeed_scraper)
        indeed_process.start()

        spider_processes = []
        for spider in self.spiders:
            p = Process(target=self.run_spider, args=(spider,))
            p.start()
            spider_processes.append(p)

        spider_processes.append(indeed_process)

        for p in spider_processes:
            p.join(self.timeout)
            if p.is_alive():
                p.terminate()
                p.join()


    def run_indeed_scraper(self):
        indeed_scraper = IndeedJobScraper(**self.job_preference)
        asyncio.run(indeed_scraper.fetch_page_content())
