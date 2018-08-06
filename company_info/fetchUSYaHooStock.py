import urllib.request
import pandas as pd,os
import ssl
import io
import json
from mongoconnect import *
import time
 
context = ssl._create_unverified_context()
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
    "Cookie": "GUC=AQEBAQFbY81cPUIetgRY&s=AQAAALBA1y1Y&g=W2J87A; cmp=t=1533542359&j=0; PRF=t%3DAAPL%252B%255EGSPTSE%252B%255EGSPC; _ga=GA1.2.775057820.1533282246; _gid=GA1.2.1389301371.1533542756; B=0t4mj8pbefn50&b=3&s=9q",
}
T = pd.read_csv(os.path.join(os.path.dirname(os.path.realpath(__file__)),'../usall.csv'))

for tid in range(len(T)):
    sym = T.iloc[tid].symbol
    url = "https://query1.finance.yahoo.com/v7/finance/download/"+ sym +"?period1=1167580800&period2=1533282206&interval=1d&events=history&crumb=F5UEf511Elc"
    request=urllib.request.Request(url, headers=headers)  
    result=urllib.request.urlopen(request, context = context, timeout=25)
    if result.code == 200 or 204:
        ts = result.read().decode('utf8')
        ts = io.StringIO(ts)
        df = pd.read_csv(ts)
        df.rename(columns={'Date':'date', 'Open':'open', 'High': 'high', 'Low':'low', 'Close':'close', 'Adj Close':'adj_close','Volume':'volume'}, inplace = True)
        records = json.loads(df.T.to_json()).values()
        us_security.insert(records)
        print(sym)
        time.sleep(3)
        # exit()