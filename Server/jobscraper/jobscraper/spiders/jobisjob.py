import re
import scrapy
from jobscraper.jobscraper.items import JobscraperItem


class JobisjobSpider(scrapy.Spider):
    name = 'jobisjob'
    allowed_domains = ['jobisjob.com']

    def __init__(self, *args, **kwargs):
        super(JobisjobSpider, self).__init__(*args, **kwargs)
        self.job = kwargs.get('job', 'Full Stack').title().replace(" ", "+")
        self.location = kwargs.get('location', 'San Lorenzo').title().replace(" ", "+")
    
    def start_requests(self):
        url = f'https://www.jobisjob.com/m/search?whatInSearchBox={self.job}&whereInSearchBox={self.location}&directUserSearch=true&page=1&order='
        self.logger.info(f'Starting requests with URL: {url}')
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for job in response.css('ul.list2 li a'):
            item = self.parse_job(job)
            if item:
                yield item

        next_page = response.css('a.button.orange::attr(href)').get()
        if next_page:
            self.logger.info(f'Following next page: {next_page}')
            yield response.follow(next_page, self.parse)

    def parse_job(self, job):
        title = job.css('div span.title::text').get()
        subtitle = job.css('div span.subtitle::text').get()
        description = job.css('span.description-text::text').get()
        date_posted_raw = job.css('span.info::text').get()
        url = job.css('::attr(href)').get()

        if not title:
            return None

        date_posted = re.sub(r'[\n\t\r]+', ' ', date_posted_raw).strip() if date_posted_raw else None
        description = re.sub(r'[\n\t\r]+', ' ', description).strip() if description else None

        organization = None
        job_location_type = None
        if subtitle:
            parts = [part.strip() for part in subtitle.split('-')]
            organization = parts[0] if len(parts) > 0 else None
            job_location_type = parts[1] if len(parts) > 1 else None

        if not organization:
            return None

        item = JobscraperItem(
            url=url,
            title=title,
            datePosted=date_posted,
            description=description,
            organization=organization,
            jobLocationType=job_location_type
        )
        return item
