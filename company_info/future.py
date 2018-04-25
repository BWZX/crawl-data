import urllib, urllib.request
from pymongo import MongoClient
__client = MongoClient('mongodb://admin:%2B@node0:27017')
future = __client.quantDay.future

def fetchData(arg):
    url = 'http://stock2.finance.sina.com.cn/futures/api/jsonp.php/data=/InnerFuturesNewService.getDailyKLine?symbol='+arg
    request=urllib.request.Request(url)  
    result=urllib.request.urlopen(request, timeout=25)
    if result.code == 200 or 204:
          
    else:
        print('request faild.')    
if __name__ == '__main__':
    fetchData('V0')  
