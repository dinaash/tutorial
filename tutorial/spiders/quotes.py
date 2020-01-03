# -*- coding: utf-8 -*-
import scrapy
import sys
from bs4 import BeautifulSoup
from scrapy.crawler import CrawlerProcess


class Caption(scrapy.Item):
    name = scrapy.Field()
    balance = scrapy.Field()

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    
    def __init__(self, *args, **kwargs): 
        super(QuotesSpider, self).__init__(*args, **kwargs)
        type = '10-K'
        print(self.dateb)
        base_url = 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={}&type={}&dateb={}'
        self.start_urls = [base_url.format(self.cik,type,self.dateb)] 
    
    def parse(self, response):
        
        doclink = ''
        soup = BeautifulSoup(response.text,'html.parser')
        table_tag = soup.find('table',class_='tableFile2')
        rows = table_tag.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            if len(cells)>3:
                if str(int((self.dateb)[:4])-1) in cells[3].text:
                    doclink='https://www.sec.gov' + cells[1].a['href']
                         
        if doclink == '':
            print("Couldn't find the document link")
            sys.exit()
        else: 
            yield scrapy.Request(doclink, callback=self.find_xblr_link)
    
    def find_xblr_link(self, response):
        xbrl_link = ''
        soup = BeautifulSoup(response.text, 'html.parser')
        table_tag = soup.find('table', class_='tableFile', summary='Data Files')
        rows = table_tag.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            if len(cells) > 3:
                if 'INS' in cells[3].text:
                    xbrl_link = 'https://www.sec.gov' + cells[2].a['href']
        if xbrl_link=='':
            print("Could not find the document link")
            sys.exit()
        else:
            yield scrapy.Request(xbrl_link, callback=self.xbrl_text)
   
    def xbrl_text(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        tag_list = soup.find_all(decimals="-6")
        filename = self.cik + '_'+ self.dateb+ '.csv' 
        with open(filename, 'w') as f:
            f.write("%s,%s\n" % ("account", "balance"))
            for tag in tag_list:
                f.write("%s,%f\n" % (tag.name, float(tag.text)))
                self.log('Saved file %s' % filename)


     


