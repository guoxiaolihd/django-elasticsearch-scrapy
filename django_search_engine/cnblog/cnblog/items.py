# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

from django_search_engine.cnblog.cnblog.elasticsearch_orm import CnblogsType


class CnblogItem(scrapy.Item):
    title = scrapy.Field()
    title_link = scrapy.Field()
    item_summary = scrapy.Field()
    post_date = scrapy.Field()

    def save_to_es(self):
        cnblog_obj = CnblogsType()
        cnblog_obj.title = self['title']
        cnblog_obj.description = self['item_summary']
        cnblog_obj.url = self['title_link']
        cnblog_obj.riqi = self['post_date']
        cnblog_obj.save()
        return
