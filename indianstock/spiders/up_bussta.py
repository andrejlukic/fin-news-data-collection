# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
from dateutil.parser import *
import re
from scrapy.loader.processors import MapCompose, Join
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join
from ..items import StockArticleItem
from ..helper import *
import hashlib

class BusStaSpider(scrapy.Spider):
    name = 'business-standard-update'
    shortn = 'bs'
    #allowed_domains = ['https://in.reuters.com']    
    start_urls = ['https://www.business-standard.com/category/markets-news-1060101.htm']    

    def parse_news(self, response):
        print('extract body, date:')

        l = ItemLoader(item=StockArticleItem(), response = response)
        l.add_xpath('date', '//meta[@itemprop="datePublished"]/@content', Join(), MapCompose(lambda x: parse(x).strftime("%Y-%m-%d %H:%M:%S")))
        l.add_css('title', 'div.main-cont-left.topB h1.headline::text')        
        l.add_css('subtitle', "div.main-cont-left.topB h2.alternativeHeadline::text")
        l.add_css('body', "div.main-cont-left.topB span.p-content p")
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('spider', self.name)
        l.add_value('scrapedate', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        return l.load_item()
        
    def parse(self, response):        
        
        base_url = 'https://www.business-standard.com'
        titles = response.css("div[class=listing-main] h2 a::text").extract()
        links  = response.css("div[class=listing-main] h2 a::attr(href)").extract()
        urls  = [base_url+link for link in links]
        hlist = [hashlib.md5(u.encode()).hexdigest() for u in urls]
        news_dict = {z[0]:list(z[1:]) for z in zip(hlist, titles, urls)}        
        h = filterAlreadyParsed(news_dict, sn = self.shortn)
        if(h):            
            for c,v in h.items():                
                yield scrapy.Request(v[1], callback=self.parse_news)
            #savenews(h)
            updatelog(h, sn = self.shortn)
        #else:
        #    print('No new news to save')
        


