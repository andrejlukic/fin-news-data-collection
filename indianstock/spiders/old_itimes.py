# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
from dateutil.parser import *
import re
import os
from scrapy.loader.processors import MapCompose, Join
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join
from ..items import StockArticleItem

class ItimesbotSpider(scrapy.Spider):
    name = 'itimesbot'
    allowed_domains = ['https://economictimes.indiatimes.com']
    
    url_list_dir = 'url lists'
    start_urls = []
    if(os.path.isdir(url_list_dir)):   
        with open(r"{}\indiatimes_infy.csv".format(url_list_dir), "rt") as f:
            start_urls = [url.strip() for url in f.readlines()]
    
    def parse(self, response):
       
        l = ItemLoader(item=StockArticleItem(), response = response)        
        # date mask: %b %d, %Y, %I.%M %p %Z
        l.add_css('date', "div.publish_on.flt::text", Join(), MapCompose(lambda x: x.replace('Updated: ', ''),
                                                                         lambda x: parse(x).strftime("%Y-%m-%d %H:%M:%S")))
        l.add_css('title', "h1.title::text")
        l.add_css('subtitle', "h2.title2::text")
        l.add_css('body', "div.Normal::text")
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('spider', self.name)
        l.add_value('scrapedate', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))        
        yield l.load_item()


