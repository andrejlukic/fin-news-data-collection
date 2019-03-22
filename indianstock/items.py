# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, Join
from w3lib.html import remove_tags, remove_tags_with_content
import regex

def filter_alphanumeric(strtoclean):
        if(not strtoclean or not strtoclean.strip()):
            return ''
        # clean up all the characters unless alphanumeric, punctuations and currencies:
        pattern = regex.compile('[^(\p{Sc})0-9a-zA-Z .,!]+')
        clean = pattern.sub('', strtoclean)
        
        return clean.strip().lower()

# remove JS tags along with content
def removeJStags(s):
    return remove_tags_with_content( s, ('script', ))

class StockArticleItem(scrapy.Item): 
         
    title = scrapy.Field(input_processor=MapCompose(filter_alphanumeric, str.strip))
    subtitle = scrapy.Field(input_processor=MapCompose(filter_alphanumeric, str.strip))
    body = scrapy.Field(output_processor=Join(), input_processor=MapCompose(removeJStags, remove_tags, filter_alphanumeric, str.strip))
    date=scrapy.Field()    
    url = scrapy.Field()
    project = scrapy.Field()
    spider = scrapy.Field()
    scrapedate = scrapy.Field()

    pass
