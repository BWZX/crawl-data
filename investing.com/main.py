import urllib, urllib.request
import requests
from pyquery import PyQuery as pq
from pandas import DataFrame as dtf
from datetime import datetime as dt
import codeconfig
import json
from pymongo import MongoClient
__client = MongoClient('mongodb://admin:%2Bbeijing2017@node0:27017')
future = __client.quantDay.future


def fetchData(arg):
    url = 'https://www.investing.com/currencies/live-currency-cross-rates'
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
    request=urllib.request.Request(url, headers=headers)  
    result=urllib.request.urlopen(request, timeout=25)
    if result.code == 200 or 204:
        ts = str(result.read())
        # print('hello')
        d = pq(ts)
        for item in d('div.liveCurrencyBoxWrap div.liveCurrencyBox').items():
            pairid = item('div').attr('data-pid')
            symbol = item('div.topBox a').text()
            # print('"'+pairid+'": "'+symbol+'",')
            # continue
            #here crawl currency
            uri = 'https://tvc4.forexpros.com/eb25a3a257581157e1844bd471b6d392/1520333930/1/1/8/history?symbol='+ pairid +'&resolution=D&from=946656000&to=2620425000'
            rdata=requests.get(uri, headers=headers).json()  
            # print(type(rdata))           
            # rdata = json.loads(rdata)
            # print(rdata['t'])
            del rdata['vo']
            del rdata['s']
            remk = False
            if rdata['v'][0] == 'n\/a':
                remk = True                
            mk_date = lambda x: dt.strftime(dt.fromtimestamp(x),'%Y-%m-%d')
            rdata = dtf(rdata)
            # print(rdata)
            rdata.rename(columns={'t':'date', 'c': 'close', 'o':'open','l':'low', 'h':'high','v':'volume'}, inplace=True)
            rdata['date']=rdata['date'].apply(mk_date)
            if remk:
                rdata['volume'] = 0
            rdata['code'] = codeconfig.codedict[pairid]
            records = json.loads(rdata.T.to_json()).values()
            future.insert(records)
            print(symbol)
            # break
        
        for item in d('table#QBS_2_inner tbody tr').items():
            pairid = item('tr').attr('pair')
            symbol = item('td a').text()
            # print('"'+pairid+'": "'+symbol+'",')
            # continue
            uri = 'https://tvc4.forexpros.com/eb25a3a257581157e1844bd471b6d392/1520333930/1/1/8/history?symbol='+ pairid +'&resolution=D&from=946656000&to=2620425000'
            rdata=requests.get(uri, headers=headers).json()

            del rdata['vo']
            del rdata['s']
            remk = False
            if rdata['v'][0] == 'n\/a':
                remk = True                
            mk_date = lambda x: dt.strftime(dt.fromtimestamp(x),'%Y-%m-%d')
            rdata = dtf(rdata)
            # print(rdata)
            rdata.rename(columns={'t':'date', 'c': 'close', 'o':'open','l':'low', 'h':'high','v':'volume'}, inplace=True)
            rdata['date']=rdata['date'].apply(mk_date)
            if remk:
                rdata['volume'] = 0
            rdata['code'] = codeconfig.codedict[pairid]
            records = json.loads(rdata.T.to_json()).values()
            future.insert(records)
            print(symbol)            

def main():
    fetchData(9)
    pass

if __name__ == '__main__':
    main()