import urllib.parse, urllib.request, json

Companies = ["ARROW GLOBAL GROUP PLC","ARTEMIS ALPHA TRUST PLC"]
Companies = [urllib.parse.quote(company) for company in Companies]

for company in Companies:
    with urllib.request.urlopen(f"https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.quotes%20where%20symbol%20in%20(%22{company}%22)&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callack=") as url:
        data = json.loads(url.read().decode())
        print(data)

    
