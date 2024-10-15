import scrapy

class JobisjobSpider(scrapy.Spider):
    name = 'jobisjob'
    
    
    allowed_domains = ['jobisjob.com']
    start_urls = ['https://www.jobisjob.com/m/search?whatInSearchBox=full+stack&whereInSearchBox=&directUserSearch=true&page=5&order=']

    def parse(self, response):
        for job in response.css('ul.list2 li a'):
            item = self.parse_job(job)
            if item != {}:
                yield item

        prev_page = response.css('a.button.orange::attr(href)').get()
        if prev_page:
            yield response.follow(prev_page, self.parse)

    def parse_job(self, job):
        
        title = job.css('div span.title::text').get()
        subtitle = job.css('div span.subtitle::text').get()

        if subtitle:
            parts = [item.strip() for item in subtitle.split('-')]
            company = parts[0] if len(parts) > 0 else None
            location = parts[1] if len(parts) > 1 else None
        else:
            company = None
            location = None
            
        if not title or not company :
            return {}

        return {
            'title': job.css('div span.title::text').get(),
            'company': company,
            'location': location,  # Handle missing location
            'link': job.css('::attr(href)').get(),
        }