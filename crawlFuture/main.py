import urllib, urllib.request
from pymongo import MongoClient
__client = MongoClient('mongodb://admin:%2B@node0:27017')
future = __client.quantDay.future

def fetchData(arg):
    url = 'http://stock2.finance.sina.com.cn/futures/api/jsonp.php/data=/InnerFuturesNewService.getDailyKLine?symbol='+arg
    request=urllib.request.Request(url)  
    result=urllib.request.urlopen(request, timeout=25)
    if result.code == 200 or 204:
        ts = str(result.read(),encoding='utf-8')
        ts = ts[:-1] 
        d = 'date'
        o = 'open'
        c = 'close'
        h = 'high'
        l = 'low'
        v = 'volume'
        ts +='\nfuture.insert(data)'       
        exec(ts)        
    else:
        print('request faild.')    
if __name__ == '__main__':
    fetchData('V0')  
