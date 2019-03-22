# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
from dateutil.parser import *
import re
from scrapy.loader.processors import MapCompose, Join
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join
from indianstock.items import StockArticleItem
import indianstock.helper as hlp
import hashlib

class ReutersSpider(scrapy.Spider):
    name = 'itimes-update'
    shortn = 'it'
    #allowed_domains = ['https://in.reuters.com']    
    start_urls = ['https://economictimes.indiatimes.com/markets/stocks/news']

    def parse_news(self, response):
        print('extract body, date:')

        l = ItemLoader(item=StockArticleItem(), response = response)
        
        # found three ways of printed dates ...
        check_date = response.xpath('//span[@itemprop="datePublished"]/@content').extract()
        if(len(check_date) == 0):
            check_date = response.xpath('//time/@datetime').extract()
            if(len(check_date) == 0):  
                l.add_css('date', "div.publish_on.flt::text", Join(), MapCompose(lambda x: x.replace('Updated: ', ''),
                                                                                 lambda x: parse(x).strftime("%Y-%m-%d %H:%M:%S")))
            else:
                l.add_xpath('date', '//span[@itemprop="datePublished"]/@content', Join(), MapCompose(lambda x: parse(x).strftime("%Y-%m-%d %H:%M:%S")))        
        l.add_css('title', 'h1.title::text')        
        l.add_css('subtitle', 'h2.title2::text')
        l.add_css('body', "div.Normal")
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('spider', self.name)
        l.add_value('scrapedate', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        return l.load_item()
        
    def parse(self, response):        
        
        base_url = 'https://economictimes.indiatimes.com'
        titles = response.css('div.tabdata div.eachStory a::text').extract()
        links  = response.css('div.tabdata div.eachStory a::attr(href)').extract()
        urls  = [base_url+link for link in links]
        hlist = [hashlib.md5(u.encode()).hexdigest() for u in urls]
        news_dict = {z[0]:list(z[1:]) for z in zip(hlist, titles, urls)}        
        h = hlp.filterAlreadyParsed(news_dict, sn = self.shortn)
        if(h):            
            for c,v in h.items():                
                yield scrapy.Request(v[1], callback=self.parse_news)
            #savenews(h)
            hlp.updatelog(h, sn = self.shortn)
        #else:
        #    print('No new news to save')
        


