# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobsgeItem(scrapy.Item):
    name = scrapy.Field()
    pass


class JobsgeItem(scrapy.Item):
    position = scrapy.Field()
    company = scrapy.Field()
    published_date = scrapy.Field()
    deadline = scrapy.Field()
    details_link = scrapy.Field()
    