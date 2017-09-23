#!/usr/bin/env python3
import urllib.parse, urllib.request, json, sys, getopt
from sys import argv

companyFile = "companylist.csv"
outputFilename = "output.csv"
tickerData = {}
columns = []
options = {}

firstColumns = ["Name", "Currency", "Ask", "Open", "PreviousClose", "PercentChange", "PriceBook", "Change", "DaysHigh", "DaysLow", "EarningsShare"]
try:
    opts, args = getopt.getopt(sys.argv[1:], "hi:o:")
except getopt.GetoptError:
    print("python endofday.py -i <inputfile>")
    sys.exit(2)    


for opt, arg in opts:
    options[opt] = arg 
    print("printing " + opt)   
 
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

for company in CompanyList:
    with urllib.request.urlopen(f"https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.quotes%20where%20symbol%20in%20(%22{company}%22)&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callack=") as url:
        data = json.loads(url.read().decode())
    quote = (data['query']['results']['quote'][0])
    tickerData[company] = quote
    
    if( len(columns) == 0):
        columns = quote.keys()
        withoutPreferredColumns = [ x for x in columns if x not in firstColumns]
        reorderedColumn = firstColumns + withoutPreferredColumns
        columns = reorderedColumn
        
    lineData = []
    for column in columns:
        lineData.append(quote[column])
    line = ",".join([ str(x) for x in lineData])
    
    if('-o' in options):
        outputFilename = options['-o']
    
    with open(outputFilename, 'w+') as file:
        print(f"{line}\n")
        file.write(f'{line}\n') 
        file.close()

    
