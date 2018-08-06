import urllib, urllib.request
from pymongo import MongoClient
from pyquery import PyQuery as pq
import pandas as pd
import json
import numpy as np
from mongoconnect import *
import os

T = pd.read_csv(os.path.join(os.path.dirname(os.path.realpath(__file__)),'../usall.csv'))

def fetchIndicators(sym):
    url = 'http://quotes.money.163.com/usstock/' + str(sym) + '_indicators.html?type=quarter'
    request=urllib.request.Request(url)  
    result=urllib.request.urlopen(request, timeout=25)
    if result.code == 200 or 204:
        ts = result.read()
        ts=ts.decode('utf8')
        # print(ts)
        d = pq(ts)
        div = d('div#list_table')
        table = []
        cell = []
        for it in div('ul li').items():
            cell.append(it.text())
        table.append(cell.copy())
        for tr in div('table tbody tr').items():
            cell = []
            for td in tr('td').items():
                cell.append(td.text())
            if len(cell) < 3:
                continue
            table.append(cell.copy())
        # import pdb;pdb.set_trace()
        tt = np.array(table)
        tt=tt.transpose()
        df = pd.DataFrame(tt, columns=['date','总市值','市盈率','市净率','市现率','市销率','总资产收益率',\
            '净资产收益率','营业毛利率','税前利润率','营业利润率','净利润率','销售收入/平均总资产','总资本回报率',\
            '总负债/总资产','普通股权益/总资产','派息比率','资本支出/销售额','流动比率','负债/息税前营业利润',\
            '速动比率','每股净资产','摊薄每股收益','每股销售额'])
        print(df)



if __name__ == '__main__':
    fetchIndicators('AAPL')


