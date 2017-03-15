#!/usr/bin/python
# -*- coding: utf-8 -*-

import tushare as ts
import config 
import json
from datetime import datetime as dt, timedelta as td
import pandas as pd
# from time_series.crawl_data import database
import database

MongodbJson={}     #输出数据爬取的开始点和结束点
try:
    with open('mongo.json','r') as f:
        MongodbJson=json.loads(f.read())
except Exception:    
    for i in config.stolist:
        MongodbJson[i]={}

def fetchAllStocksHistoryData():    
    """
        获取所有的股票的历史数据，
        不包括成交明细，同时把数据存到数据库。
        这个函数应该只运行一次        
    """
    str_price_json={
        'metric':'security.price',
        'time':'date',
        'value':'close',
        'code':'code',
        'tags':{
            'period': 'day'

        }
    }
    str_volume_json={
        'metric':'security.volume',
        'time':'date',
        'value':'volume',
        'code':'code',
        'tags':{
            'period':'day'
        }
    }

    currentCode={}
    for i in config.stolist:
        df_D=ts.get_k_data(i,'1980-01-01',ktype='D')
        df_H1=ts.get_k_data(i,'1980-01-01',ktype='60')
        df_M30=ts.get_k_data(i,'1980-01-01',ktype='30')

        currentCode['dayStart'] = df_D.iloc[0,0]
        currentCode['dayEnd']   = df_D.iloc[-1,0]
        currentCode['h1Start'] = df_D.iloc[0,0]
        currentCode['h1End']   = df_D.iloc[-1,0]
        currentCode['m30Start'] = df_D.iloc[0,0]
        currentCode['m30End']   = df_D.iloc[-1,0]
        MongodbJson[i]=currentCode.copy()

        str_volume_json['tags']['period']='day'
        str_price_json['tags']['period']='day'
        str_price_json['value']='open'
        str_price_json['tags']['price']='open'
        result=_dataFrame2MetricsList(df_D,str_price_json,time=' 15:00:00')  #转换数据成可供opentsdb输入的list
        database.insertList(result)                 #保存security.price 数据 
        str_price_json['value']='close'
        str_price_json['tags']['price']='close'
        result=_dataFrame2MetricsList(df_D,str_price_json,time=' 15:00:00')  #转换数据成可供opentsdb输入的list
        database.insertList(result)                 #保存security.price 数据 
        str_price_json['value']='high'
        str_price_json['tags']['price']='high'
        result=_dataFrame2MetricsList(df_D,str_price_json,time=' 15:00:00')  #转换数据成可供opentsdb输入的list
        database.insertList(result)                 #保存security.price 数据 
        str_price_json['value']='low'
        str_price_json['tags']['price']='low'
        result=_dataFrame2MetricsList(df_D,str_price_json,time=' 15:00:00')  #转换数据成可供opentsdb输入的list
        database.insertList(result)                 #保存security.price 数据 
        result=_dataFrame2MetricsList(df_D,str_volume_json,time=' 15:00:00')  #转换数据成可供opentsdb输入的list
        database.insertList(result)                 #保存volume 数据

        str_volume_json['tags']['period']='h1'
        str_price_json['tags']['period']='h1'
        str_price_json['value']='open'
        str_price_json['tags']['price']='open'
        result=_dataFrame2MetricsList(df_H1,str_price_json,time=':00')  #转换数据成可供opentsdb输入的list
        database.insertList(result)                 #保存security.price 数据  
        str_price_json['value']='close'
        str_price_json['tags']['price']='close'
        result=_dataFrame2MetricsList(df_H1,str_price_json,time=':00')  #转换数据成可供opentsdb输入的list
        database.insertList(result)                 #保存security.price 数据  
        str_price_json['value']='high'
        str_price_json['tags']['price']='high'
        result=_dataFrame2MetricsList(df_H1,str_price_json,time=':00')  #转换数据成可供opentsdb输入的list
        database.insertList(result)                 #保存security.price 数据  
        str_price_json['value']='low'
        str_price_json['tags']['price']='low'
        result=_dataFrame2MetricsList(df_H1,str_price_json,time=':00')  #转换数据成可供opentsdb输入的list
        database.insertList(result)                 #保存security.price 数据  
        result=_dataFrame2MetricsList(df_H1,str_volume_json,time=':00')  #转换数据成可供opentsdb输入的list
        database.insertList(result)                 #保存volume 数据

        str_volume_json['tags']['period']='m30'
        str_price_json['tags']['period']='m30'
        str_price_json['value']='open'
        str_price_json['tags']['price']='open'
        result=_dataFrame2MetricsList(df_M30,str_price_json,time=':00')  #转换数据成可供opentsdb输入的list
        database.insertList(result)                 #保存security.price 数据  
        str_price_json['value']='close'
        str_price_json['tags']['price']='close'
        result=_dataFrame2MetricsList(df_M30,str_price_json,time=':00')  #转换数据成可供opentsdb输入的list
        database.insertList(result)                 #保存security.price 数据  
        str_price_json['value']='high'
        str_price_json['tags']['price']='high'
        result=_dataFrame2MetricsList(df_M30,str_price_json,time=':00')  #转换数据成可供opentsdb输入的list
        database.insertList(result)                 #保存security.price 数据  
        str_price_json['value']='low'
        str_price_json['tags']['price']='low'
        result=_dataFrame2MetricsList(df_M30,str_price_json,time=':00')  #转换数据成可供opentsdb输入的list
        database.insertList(result)                 #保存security.price 数据  
        result=_dataFrame2MetricsList(df_M30,str_volume_json,time=':00')  #转换数据成可供opentsdb输入的list
        database.insertList(result)                 #保存volume 数据
        with open('progress.ini','w') as f:
            f.write(str(i))
    pass

def fetchAllStocksTodayNotTickData():
    str_price_json={
        'metric':'security.price',
        'time':'date',
        'value':'close',
        'code':'code',
        'tags':{
            'period': 'day'

        }
    }
    str_volume_json={
        'metric':'security.volume',
        'time':'date',
        'value':'volume',
        'code':'code',
        'tags':{
            'period':'day'
        }
    }

    for i in config.stolist:
        df_D=ts.get_k_data(i,ktype='D')
        df_H1=ts.get_k_data(i,ktype='60')
        df_M30=ts.get_k_data(i,ktype='30')

        MongodbJson[i]['dayEnd']   = df_D.iloc[-1,0]
        MongodbJson[i]['h1End']   = df_D.iloc[-1,0]
        MongodbJson[i]['m30End']   = df_D.iloc[-1,0]

        str_volume_json['tags']['period']='day'
        str_price_json['tags']['period']='day'
        str_price_json['value']='open'
        str_price_json['tags']['price']='open'
        str_price_json['tags']['price']='open'
        result=_dataFrame2MetricsList(df_D,str_price_json,time=' 15:00:00')  #转换数据成可供opentsdb输入的list
        database.insertList(result)                 #保存security.price 数据 
        str_price_json['value']='close'
        str_price_json['tags']['price']='close'
        result=_dataFrame2MetricsList(df_D,str_price_json,time=' 15:00:00')  #转换数据成可供opentsdb输入的list
        database.insertList(result)                 #保存security.price 数据 
        str_price_json['value']='high'
        str_price_json['tags']['price']='high'
        result=_dataFrame2MetricsList(df_D,str_price_json,time=' 15:00:00')  #转换数据成可供opentsdb输入的list
        database.insertList(result)                 #保存security.price 数据 
        str_price_json['value']='low'
        str_price_json['tags']['price']='low'
        result=_dataFrame2MetricsList(df_D,str_price_json,time=' 15:00:00')  #转换数据成可供opentsdb输入的list
        database.insertList(result)                 #保存security.price 数据 
        result=_dataFrame2MetricsList(df_D,str_volume_json,time=' 15:00:00')  #转换数据成可供opentsdb输入的list
        database.insertList(result)                 #保存volume 数据

        str_volume_json['tags']['period']='h1'
        str_price_json['tags']['period']='h1'
        str_price_json['value']='open'
        str_price_json['tags']['price']='open'
        result=_dataFrame2MetricsList(df_H1,str_price_json,time=':00')  #转换数据成可供opentsdb输入的list
        database.insertList(result)                 #保存security.price 数据  
        str_price_json['value']='close'
        str_price_json['tags']['price']='close'
        result=_dataFrame2MetricsList(df_H1,str_price_json,time=':00')  #转换数据成可供opentsdb输入的list
        database.insertList(result)                 #保存security.price 数据  
        str_price_json['value']='high'
        str_price_json['tags']['price']='high'
        result=_dataFrame2MetricsList(df_H1,str_price_json,time=':00')  #转换数据成可供opentsdb输入的list
        database.insertList(result)                 #保存security.price 数据  
        str_price_json['value']='low'
        str_price_json['tags']['price']='low'
        result=_dataFrame2MetricsList(df_H1,str_price_json,time=':00')  #转换数据成可供opentsdb输入的list
        database.insertList(result)                 #保存security.price 数据  
        result=_dataFrame2MetricsList(df_H1,str_volume_json,time=':00')  #转换数据成可供opentsdb输入的list
        database.insertList(result)                 #保存volume 数据

        str_volume_json['tags']['period']='m30'
        str_price_json['tags']['period']='m30'
        str_price_json['value']='open'
        str_price_json['tags']['price']='open'
        result=_dataFrame2MetricsList(df_M30,str_price_json,time=':00')  #转换数据成可供opentsdb输入的list
        database.insertList(result)                 #保存security.price 数据  
        str_price_json['value']='close'
        str_price_json['tags']['price']='close'
        result=_dataFrame2MetricsList(df_M30,str_price_json,time=':00')  #转换数据成可供opentsdb输入的list
        database.insertList(result)                 #保存security.price 数据  
        str_price_json['value']='high'
        str_price_json['tags']['price']='high'
        result=_dataFrame2MetricsList(df_M30,str_price_json,time=':00')  #转换数据成可供opentsdb输入的list
        database.insertList(result)                 #保存security.price 数据  
        str_price_json['value']='low'
        str_price_json['tags']['price']='low'
        result=_dataFrame2MetricsList(df_M30,str_price_json,time=':00')  #转换数据成可供opentsdb输入的list
        database.insertList(result)                 #保存security.price 数据  
        result=_dataFrame2MetricsList(df_M30,str_volume_json,time=':00')  #转换数据成可供opentsdb输入的list
        database.insertList(result)                 #保存volume 数据
    pass


def fetchAllStocksHistoryTickData():    
    """
        获取所有的股票的成交明细历史数据，
        同时把数据存到数据库。
        这个函数应该只运行一次        
    """
    str_price_json={
        'metric':'security.price',
        'time':'time',
        'value':'price',
        'code':'code',
        'tags':{
            'period': 'tick'
        }
    }
    str_volume_json={
        'metric':'security.volume',
        'time':'time',
        'value':'volume',
        'code':'code',
        'tags':{
            'period':'tick',
            'type': True
        }
    }

    today=dt.now()
    label=False
    today=dt(today.year, today.month, today.day)
    delta=td(1,0,0)                                 #间隔一天
    
    for i in config.stolist:
        date=dt(2013,1,1)
        while date<today:
            timestr=dt.strftime(date,'%Y-%m-%d')
            df=ts.get_tick_data(i,date=timestr)            
            timestr=timestr+' '
            if not label:             #提取tickStart
                if not df.iloc[0,0].startswith('alert'):
                    label=True
                    MongodbJson[i]['tickStart']=timestr+df.iloc[-1,0]
            result=_dataFrame2MetricsList(df,str_volume_json,date=timestr,code=i)
            database.insertList(result)
            result=_dataFrame2MetricsList(df,str_price_json,date=timestr,code=i)
            database.insertList(result)
            date=date+delta
            pass        
    pass

def fetchAllStocksTodayTickData():    
    """
        获取所有的股票当日的成交明细数据，
        同时把数据存到数据库。        
    """   
    str_price_json={
        'metric':'security.price',
        'time':'time',
        'value':'price',
        'code':'code',
        'tags':{
            'period': 'tick'

        }
    }

    str_volume_json={
        'metric':'security.volume',
        'time':'time',
        'value':'volume',
        'code':'code',
        'tags':{
            'period':'tick',
            'type': True
        }
    }

    now=dt.now()
    date=dt(now.year,now.month,now.day)
    timestr=dt.strftime(date,'%Y-%m-%d')
    for i in config.stolist:
        df=ts.get_today_ticks(i)        
        timestr=timestr+' '
        if not df.iloc[0,0].startswith('alert'):            
            MongodbJson[i]['tickEnd']=timestr+df.iloc[0,0]

        result=_dataFrame2MetricsList(df,str_volume_json,date=timestr,code=i)
        database.insertList(result)
        result=_dataFrame2MetricsList(df,str_price_json,date=timestr,code=i)
        database.insertList(result)
    pass


def fetchAllStocksCurrentTickData():    
    """
        获取所有的股票当前level1数据，
        是否存到数据库待定。

    """  

    for i in config.stolist:
        df=ts.get_realtime_quotes(i)

    pass

def _dataFrame2MetricsList(df,str_json,date='',time='',code=''):
    data=[]

    if df.iloc[0,0].startswith('alert'):
        return data

    for index, row in df.iterrows():
        if code:
            str_json['tags']['code']=code
        else:
            str_json['tags']['code']=row[str_json['code']]

        if str_json['tags'].get('type'):  #tick data will has type, shows buy/sell
            str_json['tags']['type']=row['type']
        data.append({
            "metric": str_json['metric'],
            "timestamp": int(dt.strptime(date+row[str_json['time']]+time,'%Y-%m-%d %H:%M:%S').timestamp()),
            "value": row[str_json['value']],
            "tags": str_json['tags']
        })
    return data

if __name__ == '__main__':
    fetchAllStocksHistoryData()     #this function should excute only once.
    # fetchAllStocksHistoryTickData() #this function should excute only once.
