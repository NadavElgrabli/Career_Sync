import scrapy


class JobscraperItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    datePosted = scrapy.Field()
    description = scrapy.Field()
    organization = scrapy.Field()
    jobLocationType = scrapy.Field()
