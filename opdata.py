# -*- coding: utf8 -*-
import json
import pandas as pd
import tushare as ts
from mongoconnet import *

__T = ts.trade_cal()

def get_day(code, start_date='2001-01-01', end_date='2017-10-10'):
    # if not start_date:
    #     start_date='2001-01-01'
    # if not end_date:
    #     end_date='2020-10-10'

    cursor = security.find({'code':code, 'date':{'$gte':start_date, '$lte': end_date}}).sort('date')
    df = pd.DataFrame(list(cursor))
    if df.empty:
        return df    
    del df['_id']
    t=__T[(__T.isOpen==1)&(__T.calendarDate>=start_date)&(__T.calendarDate<=end_date)]   
    t.columns=['date','isOpen']
    r=pd.merge(df,t,on='date',how='right')
    r=r.sort_values('date').reset_index()
    del r['index']
    del r['isOpen']xz
    # print(r)
    k=r.isnull()
    k=list(k[k.open==True].index)
    k.sort()
    ii=list(r.columns).index('date')
    for i in k:
        date=r.iloc[i].date
        r.iloc[i]=r.iloc[i-1]
        r.iat[i, ii] = date    
    return r



if __name__ == '__main__':
    print(get_day('000001','2017-08-05','2017-08-05'))