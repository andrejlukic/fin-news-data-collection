# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
from dateutil.parser import *
import re
from scrapy.loader.processors import MapCompose, Join
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join
from indianstock.items import StockArticleItem

class ReutersSpider(scrapy.Spider):
    name = 'reuters'
    allowed_domains = ['http://feeds.reuters.com']
    with open(r"url lists\reuter_infy.csv", "rt") as f:
        start_urls = [url.strip() for url in f.readlines()]
    
    def parse(self, response):        
        #Extracting the content using css selectors
        l = ItemLoader(item=StockArticleItem(), response = response)
        l.add_css('date', 'div.ArticleHeader_date::text', Join(), MapCompose(lambda x: re.sub(" +"," ","".join(x.split('/')[:2])).strip(),
                                                                                             lambda x: parse(x).strftime("%Y-%m-%d %H:%M:%S")))
        l.add_css('title', "h1.ArticleHeader_headline::text")
        #l.add_css('subtitle', "h2.alternativeHeadline::text")
        l.add_css('body', "div.StandardArticleBody_body")
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('spider', self.name)
        l.add_value('scrapedate', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))        
        yield l.load_item()


