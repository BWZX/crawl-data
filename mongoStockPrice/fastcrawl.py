# -*- coding: utf8 -*-
import json
import sys
sys.path.append('../publicstuff')
import config
import tushare as ts
from datetime import datetime as dt, timedelta as td
import opdata
from mongoconnet import *

def fetchAll(slist):    
    """
        获取slist 列表的股票的历史数据，
        不包括成交明细，同时把数据存到数据库。
        这个函数应该只运行一次        
    """
    for sto in slist:
        print(sto)        
        df_D=ts.get_k_data(sto,'1980-01-01',ktype='D') 
        df_D['name']=config.StocksList[sto]
        records = json.loads(df_D.T.to_json()).values()
        security.insert(records)

def fetchContinue(slist):
    """
        续爬slist列表里的股票，
        同时把数据存到数据库。
        这个函数按天运行        
    """
    mkday=lambda x: dt(x.year, x.month, x.day)    
    today=dt.today()
    today=dt(today.year, today.month, today.day)

    lastday=today-td(1,0,0)  #####
    mongoday=today-td(20,0,0)
    print(today)
    todaystr=dt.strftime(today,'%Y-%m-%d')
    lastdaystr=dt.strftime(lastday,'%Y-%m-%d')
    mongodaystr=dt.strftime(mongoday,'%Y-%m-%d')

    recrawlist=[]
    for sto in slist:
        tsdt=ts.get_k_data(sto)
        mongodt=opdata.get_day(sto,mongodaystr, lastdaystr)
        if security.count({'code':sto,'date': todaystr}) >=1:
            print('here has inserted.')
            continue
        if tsdt.empty:
            continue
        try:
            if ((tsdt[tsdt.date==todaystr].open - mongodt.iloc[-1].close)/mongodt.iloc[-1].close > 0.14).bool():
                recrawlist.append(sto)
                print(sto)
                print(mongodt.iloc[-1])
                security.delete_many({'code': sto})
                print('data delete')                
            else:
                if not tsdt[tsdt.date==todaystr].empty:
                    records = tsdt[tsdt.date==todaystr].to_dict('record')[0]
                    records['name']=config.StocksList[sto]
                    security.insert_one(records)
                    print('inset one of the code ',sto)
            pass
        except Exception:
            if not tsdt[tsdt.date==todaystr].empty:
                records = tsdt[tsdt.date==todaystr].to_dict('record')[0]
                records['name']=config.StocksList[sto]
                security.insert_one(records)
                print('Exception here but still inset one of the code ',sto)
            pass
    print('will recrawl', recrawlist)
    if recrawlist:
        fetchAll(recrawlist)        

if __name__ == '__main__':
    # fetchAll(['000002','000004','000007','000011', '000014'])
    fetchContinue(config.stolist)