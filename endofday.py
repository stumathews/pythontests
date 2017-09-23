#!/usr/bin/env python3
import urllib.parse, urllib.request, json, sys, getopt
import os
from sys import argv
import concurrent.futures
import time

start = time.time()

tickerData = {}
columns = []
options = {}
companyFile = "companylist.csv"
outputFilename = time.strftime("%Y-%m-%d-%H%M%S.csv")
append_write = 'a';

firstColumns = ["Name", "Currency", "Ask", "Open", "PreviousClose", "PercentChange", "PriceBook", "Change", "DaysHigh", "DaysLow", "EarningsShare"]
try:
    opts, args = getopt.getopt(sys.argv[1:], "hi:o:")
except getopt.GetoptError:
    print("python endofday.py -i <inputfile>")
    sys.exit(2)

for opt, arg in opts:
    options[opt] = arg
 
if('-h' in options):
    print('''Usage: ./endofday.py <options>

Options:
 -o          : output file location
 -i          : companylist file location
 
 
 Examples:  ./endofpday.pl
            ./endofday.pl -i companies.csv -o output.csv          
 
 Notes: Python3 required.
        ''')
    exit(0)
 
if('-i' in options):
    companyFile = options['-i'];
    
with open(companyFile) as f:
    content = f.readlines()
    
CompanyList = [x.strip() for x in content]
CompanyList = [urllib.parse.quote(company) for company in CompanyList]

def get_company_data(company):
    try:
        with urllib.request.urlopen(f"https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.quotes%20where%20symbol%20in%20(%22{company}%22)&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callack=") as url:
            data = json.loads(url.read().decode())
        quote = (data['query']['results']['quote'][0])    
        print(f"%7s %7s %7s\n" % (quote["Ask"], quote["Open"], quote["Symbol"]))
        return quote 
    except urllib.error.HTTPError:
        print(f"error trying to get {company} details\n")

with concurrent.futures.ProcessPoolExecutor(max_workers=2) as executor:
    for company, quote in zip(CompanyList, executor.map(get_company_data, CompanyList)):
        tickerData[company] = quote

if('-o' in options):
    outputFilename = options['-o']
    
print("writing results\n")
with open(outputFilename, 'w') as file:
    for company in tickerData.keys():
        quote = tickerData[company]
        if(len(columns) == 0):
            columns = quote.keys()
            withoutPreferredColumns = [ x for x in columns if x not in firstColumns]
            reorderedColumn = firstColumns + withoutPreferredColumns
            columns = reorderedColumn
            file.write(",".join([ str(x) for x in columns])) 
        lineData = []
        for column in columns:
            lineData.append(quote[column])
            
        line = ",".join([ str(x) for x in lineData])
        file.write(f'{line}\n')  
        print(f"wrote {line}\n")
        
print("Job took "+time.time() - start+" secs\n")
