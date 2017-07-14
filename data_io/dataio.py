#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
sys.path.append('../publicstuff')
import json
import urllib, urllib.request
from mongoModel import *
from datetime import datetime as dt, timedelta as td
import pandas as pd 
import numpy as np

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

    pass

def _getVolumeData(code, period, start, end):     #1980/01/01-00:00:00  
    url='http://u:4242/api/query?start={start}&end={end}&m=none:security.volume%7Bperiod={period},code={code}%7D'.format(start=start, end=end, period=period, code=code)    
    request=urllib.request.Request(url)  
    result=urllib.request.urlopen(request)
    if result.code == 200 or 204:
        jstr=str(result.read(),encoding = 'utf-8')
        result=json.loads(jstr)
        return result[0]['dps'] 
    #print(data)
    pass

def _rightPrice(data, security):
    try:        
        sec=Securities.objects.raw({'code':security}).all()[0]
        # print(sec._id,'  sssss')
    except Securities.DoesNotExist:
        return
    shBonus  = ShareBonus.objects.raw({'gupiao': sec._id}).all()
    shRation = ShareRation.objects.raw({'gupiao':sec._id}).all()
    # print(shBonus[3].dengjiri)
    iteration=0
    for it in shBonus:
        theday=it.dengjiri
        try:
            theday=int(dt.strptime(theday,'%Y-%m-%d').timestamp())
            theday=theday+54000
        except Exception:
            continue
        while True:
            timeiter=data[0][iteration]
            if  theday == timeiter:
                close_price=data[2][iteration]
                px=double(it.paixi)
                sg=double(it.songgu)
                zz=double(it.zhuanzeng)
                gap=(close_price-px/10.0)*(1+zz/10+sg/10)
                for ii in range(1,5):
                    data[ii][iteration]-gap
                pass
            elif timeiter>theday:
                theday=theday+1
            else:
                for ii in range(1,5):
                    data[ii][iteration]-gap
                pass
            pass
    pass

def get_price(security, start_date ='1y-ago', frequency ='day'):
    if type(security) is not type([]):
        security=[security]
    # oudata={}
    oudf={}
    for code in security:
        op = _getPriceData(code,frequency, start_date, '1s-ago', 'open')
        cl = _getPriceData(code,frequency, start_date, '1s-ago', 'close')
        lo = _getPriceData(code,frequency, start_date, '1s-ago', 'low')
        hi = _getPriceData(code,frequency, start_date, '1s-ago', 'high')
        vl = _getVolumeData(code,frequency, start_date, '1s-ago')
        # print(op)
        candle=[]
        opp=sorted(op.keys(),reverse=True) #from now to ago
        for it in opp:
            candle.append([it, op[it], cl[it], lo[it], hi[it], vl[it]])
        # print(candle)
        _rightPrice(candle, code)
        d={
            'time': pd.Series(candle[0]), 'open': pd.Series(candle[1]), 'close': pd.Series(candle[2]),
            'high': pd.Series(candle[3]), 'low': pd.Series(candle[4]), 'volume': pd.Series(candle[5])
        }
        oudf[code]=pd.DataFrame(d)
        # oudata[code]=candle.copy()
    print(oudf)
    return oudf

def get_hs300():
    hs300={}
    for obj in Hs300.objects.all():
        hs300[obj.code]=obj.name 
    return hs300
    pass

def get_sz50():
    sz50={}
    for obj in Sz50.objects.all():
        sz50[obj.code]=obj.name
    return sz50
    pass

def get_zz500():
    zz500={}
    for obj in Zz500.objects.all():
        zz500[obj.code]=obj.name
    return zz500
    pass

def get_classified(tag=[]):
    clas={}
    if len(tag)>0:
        for obj in Classified.objects.raw({'$or':[{'industry':{'$in':tag}, 'concept':{'$in':tag} }]}).all():
            # print(999)
            clas[obj.code]=obj.name
        pass
    else:
        clas=config.StocksList

    return clas
    pass

if __name__ == '__main__':
    # get_price(['000001','000002'])
    print(get_zz500())
    print(get_classified(['生物智能','None']))