from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time, re
import pandas as pd
import numpy as np


driver = webdriver.Chrome()
df = pd.DataFrame(columns=['Candidate', 'State', 'Donors'])
k = 1

candidates = [['Bernie','C00411330&committee_id=C00577130'],['Beto','C00501197'],['Warren','C00500843&committee_id=C00566752&committee_id=C00631861'],['Gillibrand','C00413914&committee_id=C00629964&committee_id=C00651943'],['Kamala','C00571919&committee_id=C00586982'],['Sherrod','C00264697'],['Merkley','C00437277&committee_id=C00553487&committee_id=C00557264'],['Booker','C00540500&committee_id=C00548586&committee_id=C00565770'],['Tulsi','C00497396&committee_id=C00542993&committee_id=C00574525'],['Klobuchar','C00410191&committee_id=C00427047&committee_id=C00431353&committee_id=C00501791&committee_id=C00628354'],['Delaney','C00508416&committee_id=C00531665']]  
states = ['IA','NH','NV','SC','CA','MA']
cycles = [2012,2014,2016,2018]
for candidate in candidates:
    for state in states:
        donor_names = []  # reset donor names
        for cycle in cycles:
            path = 'https://www.fec.gov/data/receipts/?two_year_transaction_period='+str(cycle)+'&data_type=processed&committee_id='+candidate[1]+'&min_date=01%2F01%2F'+str(cycle-1)+'&max_date=12%2F31%2F'+str(cycle)+'&contributor_state='+state+'&is_individual=true'
            driver.get(path)
            soup = BeautifulSoup(driver.page_source)   #print(soup.prettify())  #print len(soup.findAll('td',{"class": " all","scope":"row"}))  # all donor names are in td tags w these elements
            try:
                page_turns = int(re.findall('[0-9]+',re.findall("Viewing.*filtered results for",str(soup))[0])[0])/30  # # of times to turn page
            except:
                page_turns = 0
            i = -1
            while i <= page_turns + 1:
                soup = BeautifulSoup(driver.page_source) 
                tdtags = soup.findAll('td',{"class": " all","scope":"row"})
                for t in tdtags:
                    donor_names.append(str(t.text))  #print str(t.text)
                i += 1
                try:
                    driver.find_element_by_id('results_next').click() # clicks on next tab
                except:
                    pass
                time.sleep(60) # wait for page to load
        df.loc[k] = [candidate[0],state,len(set(donor_names))]
        k += 1
        print df
    print (candidate[0] + ' has ' + str(len(donor_names)) + ' donations in ' + state)
    print (candidate[0] + ' has ' + str(len(set(donor_names))) + ' unique donors in ' + state)
driver.close()
print df
df.to_csv('donor_scrape.csv')