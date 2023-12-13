# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class BanItem(scrapy.Item):
    source = scrapy.Field()
    url = scrapy.Field()
    reason = scrapy.Field()
    date = scrapy.Field()
    expires = scrapy.Field()
    
    def to_json(self):
        return {
            'source': self['source'],
            'url': self['url'],
            'reason': self['reason'],
            'date': self['date'],
            'expires': self['expires']
        }