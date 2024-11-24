import json
import scrapy
from jobscraper.jobscraper.items import JobscraperItem

class MonsterspiderSpider(scrapy.Spider):
    name = "monsterspider"
    
    def __init__(self, *args, **kwargs):
        super(MonsterspiderSpider, self).__init__(*args, **kwargs)
        
        self.job = kwargs.get('job', 'Full Stack').title()
        self.location = kwargs.get('location', 'San Lorenzo').title()
        self.username = kwargs.get('username', '')
        self.kwargs = kwargs
        
    def start_requests(self):
        url = "https://appsapi.monster.io/jobs-svx-service/v2/monster/search-jobs/samsearch/en-US?apikey=AE50QWejwK4J73X1y1uNqpWRr2PmKB3S"
        data = {
            "jobQuery": {
                "query": self.job,
                "locations": [
                    {
                        "country": "us",
                        "address": self.location,
                        "radius": {
                            "unit": "mi",
                            "value": 20
                        }
                    }
                ]
            },
            "jobAdsRequest": {
                "position": list(range(1, 10)),
                "placement": {
                    "channel": "WEB",
                    "location": "JobSearchPage",
                    "property": "monster.com",
                    "type": "JOB_SEARCH",
                    "view": "SPLIT"
                },
            },
            "fingerprintId": "z150c72f5ac7a9d8ce376f6b50376a99c",
            "offset": 0,
            "pageSize": 9,
            "searchId": "" ,
            "includeJobs": []
        }

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        
        yield scrapy.Request(
            url=url,
            method="POST",
            headers=headers,
            body=json.dumps(data),
            callback=self.parse
        )

    def parse(self, response):
        data = json.loads(response.text)
        job_list = data.get('jobResults', [])
        for job_result in job_list:
            job_posting = job_result.get('normalizedJobPosting', {})
            item = self.parse_job(job_posting)
            yield item

    def get_job_location(self, job):
        job_location = job['jobLocation'][0].get('address', {})
        addressLocality = job_location.get("addressLocality")
        addressRegion = job_location.get("addressRegion")
        addressCountry = job_location.get("addressCountry")
        return ', '.join(filter(None, [addressLocality, addressRegion, addressCountry]))

    def parse_job(self, job):
        job_item = JobscraperItem()
        job_item['title'] = job['title']
        job_item['url'] = job['url']
        job_item['description'] = job['description']
        job_item['organization'] = job['hiringOrganization']['name']
        job_item['location'] = self.get_job_location(job)
        
        return job_item


