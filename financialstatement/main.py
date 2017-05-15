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

for year in range(2000,2018):
    for quarter in range(1,5):            
        finance = ts.get_report_data(year, quarter)
        profit = ts.get_profit_data(year, quarter)
        operation = ts.get_operation_data(year, quarter)
        # time.sleep(9)
        growth = ts.get_growth_data(year, quarter)
        debtpay = ts.get_debtpaying_data(year, quarter)
        cashFlow = ts.get_cashflow_data(year, quarter)
        fundHold = ts.fund_holdings(year, quarter)
        forecast = ts.forecast_data(year, quarter)
        result = pd.concat([finance, profit, operation, growth, debtpay, cashFlow, fundHold, forecast], axis=1)
        
        for row in result.iterrows():
            args=[]
            for arg in arglist:
                args.append(row[arg])

            # sec=Securities.objects.get({'code':row['code']})
            try:
                # print(data['shareCode'])
                sec=Securities.objects.get({'code':row['code']})
            except Securities.DoesNotExist:
                # print("the share code isn't save yet, is odd.")
                # exit()
                exc=Exchange.objects.get({'name':'沪深股市'})
                sec=Securities(config.StocksList[row['code']], row['code'], exc)
            args=[sec]+args
            try:
                Finance.objects.get({'security': args[0], 'time': args[1]})
            except Finance.DoesNotExist:                
                Finance(*args).save()
            print('rough complete.')


    
