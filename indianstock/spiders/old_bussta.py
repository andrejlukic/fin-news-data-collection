# -*- coding: utf-8 -*-
import scrapy
import os
from datetime import datetime
from dateutil.parser import *
import re
from scrapy.loader.processors import MapCompose, Join
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join
from ..items import StockArticleItem

class BusinessStandardSpider(scrapy.Spider):   
    name = 'business-standard'
    allowed_domains = ['http://www.business-standard.com']
    
    url_list_dir = 'url lists'
    start_urls = []
    if(os.path.isdir(url_list_dir)):        
        with open(r"{}\businessstandard_infy.csv".format(url_list_dir), "rt") as f:
            start_urls = [url.strip() for url in f.readlines()]
    
    def parse(self, response):        
        l = ItemLoader(item=StockArticleItem(), response = response)
        l.add_xpath('date', '//meta[@itemprop="datePublished"]/@content', Join(), MapCompose(lambda x: parse(x).strftime("%Y-%m-%d %H:%M:%S")))
        l.add_css('title', "h1.headline::text")
        l.add_css('subtitle', "h2.alternativeHeadline::text")
        l.add_css('body', "span.p-content")
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('spider', self.name)
        l.add_value('scrapedate', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))        
        yield l.load_item()


