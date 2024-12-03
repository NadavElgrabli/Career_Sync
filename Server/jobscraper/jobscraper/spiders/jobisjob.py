import re
import scrapy
from jobscraper.jobscraper.items import JobscraperItem
from urllib.parse import urljoin

class JobisjobSpider(scrapy.Spider):
    name = 'jobisjob'
    allowed_domains = ['jobisjob.com']

    def __init__(self, *args, **kwargs):
        super(JobisjobSpider, self).__init__(*args, **kwargs)
        self.job = kwargs.get('job', 'Full Stack').title().replace(" ", "+")
        self.location = kwargs.get('location', 'San Lorenzo').title().replace(" ", "+")
        self.username = kwargs.get('username', '')
        self.max_job_search = 2
        self.jobs_scraped = 0
        self.kwargs = kwargs
        
    def start_requests(self):
        url = f'https://www.jobisjob.com/m/search?whatInSearchBox={self.job}&whereInSearchBox={self.location}&directUserSearch=true&page=1&order='
        self.logger.info(f'Starting requests with URL: {url}')
        yield scrapy.Request(url=url, callback=self.parse)
        
    def parse(self, response):
        
        job_links = response.css('ul.list2 li a::attr(href)').getall()
        for link in job_links:
            
            if self.jobs_scraped >= self.max_job_search:
                return
            yield response.follow(link, self.parse_job)
            
            
    def parse_job(self, response):
        self.jobs_scraped += 1  
        detail = response.css('ul.details li')
        
        organization = response.css('ul.details li p.text::text')[0].get() if len(detail) > 0 else None
        location = response.css('ul.details li p.text::text')[1].get() if len(detail) > 1 else None
        
        title = response.css('p.title::text').get()
        raw_url = response.css('div#offer-actions ul li a::attr(href)').get()
        url = urljoin(response.url, raw_url) if raw_url else response.url
        description_element = response.css('div#description_text').get()
        if (not description_element):
            return
        description = re.sub(r'\s+', ' ', description_element.strip()).lstrip('\n ')
        
        item = JobscraperItem(
            url=url,
            title=title,
            description=description,
            organization=organization,
            location=location
        )
        yield item

        


