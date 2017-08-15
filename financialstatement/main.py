#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
sys.path.append('../publicstuff')
import config
import tushare as ts
import pandas as pd
import sys
import time
from mongoModel import *
# Exchange(name='沪深股市').save()

for year in range(2004,2018):
    for quarter in range(1,5):            
        finance = ts.get_report_data(year, quarter)
        profit = ts.get_profit_data(year, quarter)
        operation = ts.get_operation_data(year, quarter)
        # time.sleep(9)
        
        debtpay = ts.get_debtpaying_data(year, quarter)
        cashFlow = ts.get_cashflow_data(year, quarter)
        fundHold = ts.fund_holdings(year, quarter)
        forecast = ts.forecast_data(year, quarter)
        growth = ts.get_growth_data(year, quarter)
        result = pd.concat([finance, profit, operation, growth, debtpay, cashFlow, fundHold, forecast], axis=1)
        for i in range(len(result)):
            it=result.iloc[i].to_dict()
            # print(it)
            # print(result.loc[i]['code'].all(),'kksksksk ',it['code'])
            if (type(it['code']) is type(0.9)) or (not it['code']):
                # print('ssssssssssssssssssssssssssssssssss')
                continue
            args=[]
            print('should insert something')
            for arg in arglist:
                args.append(it.get(arg))

            # sec=Securities.objects.get({'code':it.get('code')})
            try:
                sec=Securities.objects.get({'code':it.get('code')})
            except Securities.DoesNotExist:
                # print("the share code isn't save yet, is odd.")
                # exit()
                # print(it)
                thename=config.StocksList.get(it.get('code'))
                if not thename:
                    thename='temp'
                exc=Exchange.objects.get({'name':'沪深股市'})
                # print(config.StocksList.get(it.get('code')),'^^^ ', it.get('code'))
                sec=Securities(thename, it.get('code'), exc).save()
            args=[sec._id]+args
            print(args)
            try:
                Finance.objects.get({'security': args[0], 'time': args[1]})
            except Finance.DoesNotExist:                
                Finance(*args).save()
            print('rough complete.')


    
