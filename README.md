# Scraping financial news using scrapy

Scraper consists of three spiders, IndiaTimes, Reuters and BusinessStandard and uses scrapy.

### Description

There are two types of spiders, one for gathering fresh news, the other for following a list of (manually prepared urls).

Spider which collects fresh news follows these steps:
1. open frontpage, gather links in the news section
2. Filter out already parsed articles using MD5 hash of each link and a hash log
3. Parse new articles:
** title
** date
** body
4. Perform basic cleaning of data:
** remove all chars excluding alphanumeric characters, punctuation and currency symbols
** trim every field
** parse date times and convert to datetime type
5. Save to CSV, semicolon delimited, enclosed in double quotes

### How to periodically run individual spiders on Windows using scrapyd

Scraping can be done periodically on a Windows machine using scrapyd and regular windows task scheduler. To set this up follow these steps:
1. install scrapyd
2. install scrapyd-client (I bumped into a problem when using pip to install scrapyd-client and it didn't install correctly. It worked when I insalled it directly from the repo: pip install git+https://github.com/scrapy/scrapyd-client)
3. run scrapyd
4. deploy the project to scrapyd:
  1. cd into the scrapy project
  2. prepare scrapy.cfg
  3. run: scrapyd-client deploy
5. check if it works by running: "curl http://local-url-to-scrapyd/schedule.json -d project=myscrapyproject -d spider=spidername". The resulst should be something like this: "{"node_name": "FACA", "status": "ok", "jobid": "811557ee4bf411e982c19cb6d0d30648"}"
6. Add a Windows Scheduled Task by running this command: schtasks /create /sc minute /mo 5 /tn TaskName /tr "cmd.exe 'curl --silent http://local-url-to-scrapyd/schedule.json -d project=myprojectname -d spider=myspidername'"
