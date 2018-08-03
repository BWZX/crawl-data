import urllib.request
import pandas as pd,os

T = pd.read_csv(os.path.join(os.path.dirname(os.path.realpath(__file__)),'usall.csv'))
url = "https://query1.finance.yahoo.com/v7/finance/download/AAPL?period1=1530603806&period2=1533282206&interval=1d&events=history&crumb=F5UEf511Elc"

for tid in range(len(T)):
    sym = T.iloc[tid].symbol
    url = "https://query1.finance.yahoo.com/v7/finance/download/"+ sym +"?period1=1530603806&period2=1533282206&interval=1d&events=history&crumb=F5UEf511Elc"
    # df = pd.read_csv(url)
    # print(df)
    # exit()
    request=urllib.request.Request(url)  
    result=urllib.request.urlopen(request, timeout=25)
    if result.code == 200 or 204:
        ts = result.read()
        df = pd.read_csv(ts)
        print(df)
        exit()

