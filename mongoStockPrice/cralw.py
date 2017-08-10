import sys
sys.path.append('../publicstuff')
import tushare as ts
import config 
import json
from datetime import datetime as dt, timedelta as td
from mongoModel import *

print('im here.')

refill_lists=[]

def fetchAllStocksHistoryData(slist):    
    """
        获取所有的股票的历史数据，
        不包括成交明细，同时把数据存到数据库。
        这个函数应该只运行一次        
    """
    trade_days = ts.trade_cal()
    
    for sto in slist:        
        df_D=ts.get_k_data(sto,'1980-01-01',ktype='D') 
        print(sto)             
        lastprice=df_D.iloc[0]['close']
        trade_days_index=trade_days[trade_days.calendarDate==df_D.iloc[0]['date']].index.tolist()[0]
        while trade_days_index<len(trade_days):
            tem=trade_days.iloc[trade_days_index]
            if tem.isOpen:
                if not df_D[df_D.date==tem.calendarDate].empty:
                    l=df_D[df_D.date==tem.calendarDate].to_dict('records')[0]
                    l=[l['date'], l['open'], l['close'], l['high'], l['low'], l['volume'], l['code']]
                    l[0]=dt.strptime(l[0],'%Y-%m-%d')
                    l=l+[config.StocksList[sto]]
                    lastprice=l[2]

                    ll=list(security.objects.raw({'date':tem.calendarDate, 'code':sto}))
                    if not ll:
                        security(*l).save() 
                    else:
                        security.objects.raw({'date':tem.calendarDate, 'code':sto}).update(
                            {'$set':{'open':l[1], 'close': l[2], 'high': l[3], 'close': l[4]}})
                
                else:
                    ll=list(security.objects.raw({'date':tem.calendarDate, 'code':sto}))
                    if not ll:
                        security(tem.calendarDate, lastprice, lastprice,lastprice,lastprice, 0, sto, config.StocksList[sto]).save()
                    else:
                        security.objects.raw({'date':tem.calendarDate, 'code':sto}).update(
                            {'$set':{'open':lastprice, 'close': lastprice, 'high': lastprice, 'close': lastprice}})
            trade_days_index+=1



def CrawlContinue():
    todayall=ts.get_today_all()
    today=dt.today()
    today=dt(today.year, today.month, today.day)
    for i in range(len(todayall)):
        tem=todayall.iloc[i]
        lastprice=tem.settlement
        if tem.open<0.001:
            ll=list(security.objects.raw({'date':today, 'code':tem.code}))
            if not ll:
                security(today, lastprice, lastprice,lastprice,lastprice, 0, tem.code, tem['name']).save()
            else:
                security.objects.raw({'date':today, 'code':tem.code}).update(
                    {'$set':{'open':lastprice, 'close': lastprice, 'high': lastprice, 'low': lastprice}})
        elif abs((tem.open-tem.settlement)/tem.settlement)>0.125:
            refill_lists.append(tem.code)
            continue
        else:
            ll=list(security.objects.raw({'date':today, 'code':tem.code}))
            if not ll:
                security(today, tem.open, tem.trade,tem.high,tem.low, tem.volume, tem.code, tem['name']).save()
            else:
                security.objects.raw({'date':today, 'code':tem.code}).update(
                    {'$set':{'open':tem.open, 'close': tem.trade, 'high': tem.high, 'low': tem.low}})

    if not refill_lists:
        fetchAllStocksHistoryData(refill_lists)
        refill_lists.clear()
    pass

def get_k_data(codes, start_date, end_date, rt_type='df'):
    start_date = dt.strptime(start_date,'%Y-%m-%d')
    end_date = dt.strptime(end_date,'%Y-%m-%d')
    dt.strptime(l[0],'%Y-%m-%d')
    if type(codes) is not type([]):
        codes = [codes]

    out={}
    outf={}
    for code in codes:
        kid=[]
        for item in security.objects.raw({'code':code, 'start_date':{'$gte':start_date},'end_date':{'$lte':end_date}}).all():
            kid.append([item.date, item.code, item.open, item.close, item.low, item.high, item.volume])
        out[code]=kid.copy()
        outf[code]=pd.DataFrame(kid, columns=['time','open','close','low','high','volume'])
    if rt_type=='df':
        return outf
    if rt_type=='array':
        return out
    pass

if __name__ == '__main__':
    if len(list(security.objects.raw({'code':'601933'})))<100:
        fetchAllStocksHistoryData(config.stolist)
    elif config.refill_list:
        fetchAllStocksHistoryData(config.refill_list)
    
    CrawlContinue()


