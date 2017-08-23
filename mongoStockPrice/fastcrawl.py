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

def fetchContinue(slist, fillDays=20):
    """
        续爬slist列表里的股票，
        同时把数据存到数据库。
        这个函数按天运行        
    """
    mkday=lambda x: dt(x.year, x.month, x.day)    
    today=dt.today()
    today=dt(today.year, today.month, today.day)

    lastday=today-td(1,0,0)  #####
    mongoday=today-td(fillDays,0,0)
    fmt = lambda x: dt.strftime(x,'%Y-%m-%d')
    todaystr=fmt(today)
    lastdaystr=fmt(lastday)
    mongodaystr=fmt(mongoday)

    recrawlist=[]
    for sto in slist:
        tsdt=ts.get_k_data(sto)
        if tsdt.empty:
            continue
        mongodt=opdata.get_day(sto,mongodaystr, todaystr)
        date=mongodt.iloc[0].date
        
        if (tsdt[tsdt.date==date].open - mongodt.iloc[0].open) > 0.00001:
            recrawlist.append(sto)
            print(sto)
            print(mongodt.iloc[-1])
            security.delete_many({'code': sto})
            print('data delete') 
            continue               

        for i in range(len(mongodt)):
            date=mongodt.iloc[i].date
            if security.count({'code':sto,'date': date}) >=1:
                print('here has inserted.')
                continue
            if not tsdt[tsdt.date==date].empty:
                records = tsdt[tsdt.date==date].to_dict('record')[0]
                records['name']=config.StocksList[sto]
                security.insert_one(records)
                print('inset one of the code ',sto)   
        
    print('will recrawl', recrawlist)
    if recrawlist:
        fetchAll(recrawlist)        


def fastContinue():
    today=dt.today()
    today=dt(today.year, today.month, today.day)
    todaystr=dt.strftime(today,'%Y-%m-%d')

    ff=ts.get_today_all()
    ff.rename(colunms={'trade':'close'}, inplace=True)
    colist=['code','name','open','high','low','close','volume']
    for co in ff.columns:
        if co not in colist:
            del ff[co]
    ff['date']=todaystr
    records = json.loads(ff.T.to_json()).values()
    security.insert(records)
    pass


if __name__ == '__main__':
    # fetchAll(['000002','000004','000007','000011', '000014'])
    fetchContinue(config.stolist[23:])