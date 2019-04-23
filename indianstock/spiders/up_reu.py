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

class ReutersSpider(scrapy.Spider):
    name = 'reuters-update'
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
        


