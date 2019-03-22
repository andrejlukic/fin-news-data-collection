# -*- coding: utf-8 -*-
import hashlib
import csv
import os

def filterAlreadyParsed(news_dict, sn=None):
        if(not news_dict):            
            return
        hold = getLastNewsHash(10, sn)
        if(not hold):            
            return news_dict
        else:            
            result = dict()                                                  
            return {nh:news_dict[nh] for nh in news_dict if nh not in hold}
        
def updatelog(news_dict, sn=None):
    fn = 'log.dat'
    if(sn):
        fn = fn.replace('.','-'+sn+'.')
    if(news_dict):
        with open(fn, 'a') as f:
            for h, title_url in news_dict.items():                    
                f.write(h+'\n')
                
def savenews(news_dictn, sn=None):
    fn = 'news.csv'
    if(sn):
        fn = fn.replace('.','-'+sn+'.')
    if(news_dict):
        with open(fn, 'a') as f:
            for h, title_url in news_dict.items():
                writer = csv.writer(f, quoting=csv.QUOTE_ALL)
                writer.writerow(title_url)

def getLastNewsHash(n, sn=None):
    
    fn = 'log.dat'
    if(sn):
        fn = fn.replace('.','-'+sn+'.')        
    if(not os.path.isfile(fn)):        
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
