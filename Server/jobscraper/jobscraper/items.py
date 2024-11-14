import scrapy


class JobscraperItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    organization = scrapy.Field()
    location = scrapy.Field()
    job_type = scrapy.Field()
    job_preference = scrapy.Field()
