# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
from dateutil.parser import *
import re
from scrapy.loader.processors import MapCompose, Join
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join
from indianstock.items import StockArticleItem
import hashlib
import csv
import os

def filterAlreadyParsed(news_dict):
        if(not news_dict):            
            return
        hold = getLastNewsHash(10)
        if(not hold):            
            return news_dict
        else:            
            result = dict()                                                  
            return {nh:news_dict[nh] for nh in news_dict if nh not in hold}
        
def updatelog(news_dict):
    if(news_dict):
        with open('log.dat', 'a') as f:
            for h, title_url in news_dict.items():                    
                f.write(h+'\n')
                
def savenews(news_dict):
    if(news_dict):
        with open('news.csv', 'a') as f:
            for h, title_url in news_dict.items():
                writer = csv.writer(f, quoting=csv.QUOTE_ALL)
                writer.writerow(title_url)

def getLastNewsHash(n):
    if(not os.path.isfile('log.dat')):        
        return None

    with open('log.dat', 'r+') as f:
        lines = f.readlines()
        if(lines and len(lines) > 0):
            i=len(lines)
            if(i > n):
                i = n            
            return [h.rstrip() for h in lines[-i:]]
        else:            
            return None    
    
class ReutersSpider(scrapy.Spider):
    name = 'reuters_update'
    #allowed_domains = ['https://in.reuters.com']    
    start_urls = ['https://in.reuters.com/finance/markets']    

    def parse_news(self, response):
        print('extract body, date:')

        l = ItemLoader(item=StockArticleItem(), response = response)
        l.add_css('date', 'div.ArticleHeader_date::text', Join(), MapCompose(lambda x: re.sub(" +"," ","".join(x.split('/')[:2])).strip(),
                                                                                             lambda x: parse(x).strftime("%Y-%m-%d %H:%M:%S")))
        l.add_css('title', "h1.ArticleHeader_headline::text")        
        l.add_css('body', "div.StandardArticleBody_body")
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('spider', self.name)
        l.add_value('scrapedate', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        return l.load_item()
        
    def parse(self, response):        
        
        base_url = 'https://in.reuters.com'
        titles = response.css("section[id=tab-markets-asia] article.story a h3::text").extract()
        links  = response.css("section[id=tab-markets-asia] article.story a")
        urls  = [base_url+link.attrib['href'] for link in links]
        hlist = [hashlib.md5(u.encode()).hexdigest() for u in urls]
        news_dict = {z[0]:list(z[1:]) for z in zip(hlist, titles, urls)}        
        h = filterAlreadyParsed(news_dict)
        if(h):            
            for c,v in h.items():                
                yield scrapy.Request(v[1], callback=self.parse_news)
            #savenews(h)
            updatelog(h)
        #else:
        #    print('No new news to save')
        


