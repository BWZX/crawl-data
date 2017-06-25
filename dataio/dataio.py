#!/usr/bin/python
# -*- coding: utf-8 -*-


def _getPriceData(code, period, start, end, price):    
    url='http://u:4242/api/query?start={start}&end={end}&m=none:security.price%7Bperiod={period},code={code},price={price}%7D'.format(start=start, end=end, period=period, code=code, price=price)    
    print(url)
    request=urllib.request.Request(url)  
    result=urllib.request.urlopen(request, timeout=25)
    if result.code == 200 or 204:
        jstr=str(result.read(),encoding='utf-8')
        result=json.loads(jstr)
        return result[0]['dps']
    else:
        print('\n数据还未保存！！\n')
    #print(data)
    pass

def _getVolumeData(code, period, start, end):     #1980/01/01-00:00:00  
    url='http://u:4242/api/query?start={start}&end={end}&m=none:security.volume%7Bperiod={period},code={code}%7D'.format(start=start, end=end, period=period, code=code)    
    request=urllib.request.Request(url)  
    result=urllib.request.urlopen(request)
    if result.code == 200 or 204:
        jstr=str(result.read(),encoding='utf-8')
        result=json.loads(jstr)
        return result[0]['dps'] 
    #print(data)
    pass

def get_price(security, start_date='1y-ago', end_date='1s-ago', frequency='day', fq='pre'):
    if type(security) is not type([]):
        security=[security]
    for code in security:
        op = _getPriceData(code,frequency, start_date, end_date, 'open')
        cl = _getPriceData(code,frequency, start_date, end_date, 'close')
        lo = _getPriceData(code,frequency, start_date, end_date, 'low')
        hi = _getPriceData(code,frequency, start_date, end_date, 'high')
