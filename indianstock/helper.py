# -*- coding: utf-8 -*-
import hashlib
import csv
import os

def filterAlreadyParsed(news_dict, sn=None):
        if(not news_dict):            
            return
        hold = getLastNewsHash(100, sn)
        if(not hold):            
            return news_dict
        else:            
            result = dict()                                                  
            return {nh:news_dict[nh] for nh in news_dict if nh not in hold}
        
def updatelog(news_dict, sn=None):
    if(sn):
        fn = 'log-{}.dat'.format(sn)
    else:
        fn = 'log.dat'

    if(news_dict):
        with open(fn, 'a') as f:
            for h, title_url in news_dict.items():                    
                f.write(h+'\n')
                
def savenews(news_dict, sn=None):
    fn = 'news.csv'
    if(sn):
        fn = fn.replace('.','-'+sn+'.')
    if(news_dict):
        with open(fn, 'a') as f:
            for h, title_url in news_dict.items():
                writer = csv.writer(f, quoting=csv.QUOTE_ALL)
                writer.writerow(title_url)

def getLastNewsHash(n, sn=None):    
    
    if(sn):
        fn = 'log-{}.dat'.format(sn)
    else:
        fn = 'log.dat'
    
    if(not os.path.isfile(fn)):
        print('{} not found'.format(fn))
        return None

    with open(fn, 'r+') as f:
        lines = f.readlines()
        if(lines and len(lines) > 0):
            i=len(lines)
            if(i > n):
                i = n            
            return [h.rstrip() for h in lines[-i:]]
        else:            
            return None    
