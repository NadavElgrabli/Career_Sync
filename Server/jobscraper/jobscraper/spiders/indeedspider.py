import scrapy
from scrapy.http import Request

class IndeedspiderSpider(scrapy.Spider):
    name = "indeedspider"

    # Custom settings to enable cookies and handle other settings at the spider level
    custom_settings = {
        'COOKIES_ENABLED': True,  # Enable cookies to handle session tracking
        'DOWNLOAD_DELAY': 1,      # Delay to avoid triggering anti-scraping mechanisms
    }

    def start_requests(self):
        url = "https://www.indeed.com/jobs?q=full+stack&l=remote&ts=1729499545404&from=searchOnHP&rq=1&rsIdx=1&fromage=last&vjk=8e448e208480d912"
    

        yield scrapy.Request(
            
            url=url,
            method="GET",
            callback=self.parse
        )
    
    def parse(self, response):
        # Handle parsing the job data here
        pass
