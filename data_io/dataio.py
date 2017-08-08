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
import tushare as ts

trade_days={}
__trade_days = ts.trade_cal()
for i,row in __trade_days.iterrows():
    t=dt.strptime(row['calendarDate'],'%Y-%m-%d')
    trade_days[t]=row['isOpen']

# print(trade_days)
assert type(trade_days[t]) is type(0)




def _getPriceData(code, period, start, end, price):    
    url='http://node0:4242/api/query?start={start}&end={end}&m=none:security.price%7Bperiod={period},code={code},price={price}%7D'.format(start=start, end=end, period=period, code=code, price=price)    
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
    url='http://node0:4242/api/query?start={start}&end={end}&m=none:security.volume%7Bperiod={period},code={code}%7D'.format(start=start, end=end, period=period, code=code)    
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

def get_price(security, start_date ='1y-ago', end_date='1s-ago', frequency ='day'):
    if type(security) is not type([]):
        security=[security]

    try:
        tmp_s_date = dt.strptime(start_date, '%Y-%m-%d')
        tmp_e_date = dt.strptime(end_date, '%Y-%m-%d')
        startdate = int(tmp_s_date.timestamp())
        enddate = int(tmp_e_date.timestamp())
        pass
    except Exception:
        tmp_s_date=start_date
        tmp_e_date=end_date
        startdate = start_date
        enddate = end_date

    

    # oudata={}
    oudf={}
    for code in security:
        op = _getPriceData(code,frequency, startdate, enddate, 'open')
        cl = _getPriceData(code,frequency, startdate, enddate, 'close')
        lo = _getPriceData(code,frequency, startdate, enddate, 'low')
        hi = _getPriceData(code,frequency, startdate, enddate, 'high')
        vl = _getVolumeData(code,frequency, startdate, enddate)
        # print(op)
        candle=[]
        opp=sorted(op.keys(),reverse=True) #from now to ago
        for it in opp:
            candle.append([it, op[it], cl[it], lo[it], hi[it], vl[it]])
        print(len(candle))
        _rightPrice(candle, code)
        _fillHalt(candle, startdate, enddate)
        print(len(candle))                
        oudf[code]=pd.DataFrame(candle,columns=['time','open','close','low','high','volume'])
        # oudata[code]=candle.copy()
    # print(oudf)
    return oudf

def _fillHalt(candle, starttime, endtime):
    fmt = lambda x: dt.fromtimestamp(float(starttime))
    mkdt = lambda x: dt(x.year, x.month, x.day)     
    try:
        endtime   = fmt(endtime) 
        starttime = fmt(starttime)        
    except Exception:
        return     
    starttime =mkdt(starttime)
    endtime = mkdt(endtime)
    loop=starttime
    index=0   

    while  loop<=endtime: 
        if not trade_days.get(loop):
            loop+=td(1,0,0)
            continue       
        if (trade_days.get(loop) and loop == mkdt(fmt(candle[index][0]))):
            loop+=td(1,0,0) 
            index+=1
            continue      

        if trade_days.get(loop) and loop < mkdt(fmt(candle[index][0])):  #today is trade day, and the nearest forward candle isn't contain the day
            pp=candle[index].copy()
            pp[0]=int(pp[0]+td(1,0,0).total_seconds())
            pp[5]=0
            candle=candle[0:index]+[pp]+candle[index:]
            loop=loop+td(1,0,0)

        if trade_days.get(loop) and loop > mkdt(fmt(candle[index][0])):
            pp=candle[index].copy()
            pp[0]=int(pp[0]+td(1,0,0).total_seconds())
            pp[5]=0
            candle=candle[0:index]+[pp]+candle[index:]
            loop=loop+td(1,0,0)
            if index+1<len(candle):
                index+=1
            pass

    # print(candle)


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
    get_price('000002','2011-10-09','2012-01-01')
    # print(get_zz500())
    # print(get_classified(['生物智能','None']))