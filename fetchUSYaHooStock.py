import urllib.request
import pandas as pd,os
import ssl
import io
 
context = ssl._create_unverified_context()
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
    "Cookie": "B=9i1d97hddv0o3&b=3&s=l8; GUC=AQEBAQFbGrlcAUIcNwQg&s=AQAAAHowfWiF&g=WxlwYQ; ucs=lnct=1528393814; cmp=t=1533392578&j=0; PRF=t%3DAPL%26fin-trd-cue%3D1"
}
T = pd.read_csv(os.path.join(os.path.dirname(os.path.realpath(__file__)),'usall.csv'))
url = "https://query1.finance.yahoo.com/v7/finance/download/AAPL?period1=1167580800&period2=1533282206&interval=1d&events=history&crumb=v3jujSqqJTG"

for tid in range(len(T)):
    sym = T.iloc[tid].symbol
    url = "https://query1.finance.yahoo.com/v7/finance/download/"+ sym +"?period1=1167580800&period2=1533282206&interval=1d&events=history&crumb=v3jujSqqJTG"
    request=urllib.request.Request(url, headers=headers)  
    result=urllib.request.urlopen(request, context = context, timeout=25)
    if result.code == 200 or 204:
        ts = result.read().decode('utf8')
        ts = io.StringIO(ts)
        df = pd.read_csv(ts)
        print(df)
        exit()

