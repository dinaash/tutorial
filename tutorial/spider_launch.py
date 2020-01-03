# -*- coding: utf-8 -*-
import spiders.quotes as quotes
import datetime

myCIKs= []

def runQuotesSpider():

    # Prompt for a CIK and save it in a list
    myCIK = 0
    while myCIK != 'y':
        myCIK = input("Enter CIK or press 'y' to exit: ")
        if myCIK != 'y':
            myCIKs.append(myCIK)
    
    #Set the number of 10K filings for a given CIK
    myYears = []
    currentyear = datetime.datetime.now().year

    for year in range(currentyear, currentyear-7,-1): #adjust number of years
        prior_to_date = str(year)+'0101'
        myYears.append(prior_to_date)
    
    #Get data into files 
    process = quotes.CrawlerProcess() 
    for cik in myCIKs:
        for yyyymmdd in myYears:
            process.crawl(quotes.QuotesSpider,cik=cik, dateb=yyyymmdd)

    process.start()
   
    

