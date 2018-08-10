import urllib, urllib.request
from pymongo import MongoClient
from pyquery import PyQuery as pq
import pandas as pd
import json
import numpy as np
from mongoconnect import *
import os
import time

T = pd.read_csv(os.path.join(os.path.dirname(os.path.realpath(__file__)),'../usall.csv'))

def fetchIndicators(sym, quarter = True): 
    """Crawled to VSAT."""
    if quarter: 
        url = 'http://quotes.money.163.com/usstock/' + str(sym) + '_indicators.html?type=quarter'
    else:
        url = 'http://quotes.money.163.com/usstock/' + str(sym) + '_indicators.html'
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
        if len(table) < 2:
            if not url.endswith('quarter'):
                return
            return fetchIndicators(sym,False)

        tt = np.array(table)
        tt=tt.transpose()
        df = pd.DataFrame(tt, columns=['date','总市值','市盈率','市净率','市现率','市销率','总资产收益率',\
            '净资产收益率','营业毛利率','税前利润率','营业利润率','净利润率','销售收入/平均总资产','总资本回报率',\
            '总负债/总资产','普通股权益/总资产','派息比率','资本支出/销售额','流动比率','负债/息税前营业利润',\
            '速动比率','每股净资产','摊薄每股收益','每股销售额'])
        df['code'] = sym
        records = json.loads(df.T.to_json()).values()
        us_finance.insert(records)
        print(sym)
        time.sleep(3)

def fetchBalance(sym, quarter = True): 
    """crawled to TRMB""" 
    if quarter: 
        url = 'http://quotes.money.163.com/usstock/' + str(sym) + '_balance.html?type=quarter'
    else:
        url = 'http://quotes.money.163.com/usstock/' + str(sym) + '_balance.html'
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
        if len(table) < 2:
            if not url.endswith('quarter'):
                return
            return fetchIndicators(sym,False)

        tt = np.array(table)
        tt=tt.transpose()
        if len(tt[0]) ==29:
            columns=['date','流动资产', '现金和短期投资', '现金', '短期应收账款', '存货', '其他流动资产', '投资和预付款', '长期应收票据', \
            '无形资产', '固定资产、厂房和设备', '递延税资产', '其他资产', '总投资', '总资产', '流动负债', '短期债务', \
            '应付账款', '应交税费', '其他流动负债', '长期债务', '递延税负债', '其他负债', '总负债', '股东权益', \
            '少数股东权益', '归属于母公司股东的权益', '总股本', '每股净资产']
        else:
            columns = ['date', '现金及同业拆借款', '银行证券投资', '发放贷款净额', '客户承兑责任', '投资性房地产', \
            '应收利息', '固定资产、厂房和设备', '递延所得税资产', '其他资产', '长期股权投资', \
            '总资产', '客户存款总额', '债务总额', '风险费用计提', '递延税负债', '其他负债', \
            '总负债', '股东权益', '少数股东权益', '归属于母公司股东的权益', '优先股账面价值', \
            '普通股权益总额', '总股本', '每股净资产', '一级资本', '二级资本']

        df = pd.DataFrame(tt, )
        df['code'] = sym
        records = json.loads(df.T.to_json()).values()
        us_balance.insert(records)
        print(sym,' balance table crawled.')
        # print(df)
        time.sleep(3)

def fetchIncome(sym, quarter = True): 
    """crawled to TRMB""" 
    if quarter: 
        url = 'http://quotes.money.163.com/usstock/' + str(sym) + '_income.html?type=quarter'
    else:
        url = 'http://quotes.money.163.com/usstock/' + str(sym) + '_imcome.html'
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
        if len(table) < 2:
            if not url.endswith('quarter'):
                return
            return fetchIndicators(sym,False)

        tt = np.array(table)
        tt=tt.transpose()
        if len(tt[0]) == 22:
            columns=['date','营业收入', '营业成本', '营业毛利', '销售、管理和行政费用', '其他费用', \
            '息税前营业利润', '营业外收支净额', '利息支出', '非经常性损益', '利润总额（税前）', \
            '所得税', '未合并的子公司利润', '其他调整', '合并净利润', '少数股东损益', '归属于母公司的净利润', \
            '优先股股息', '归属于普通股东的综合收益', '普通股本', '基本每股收益', '本期每股红利']
        else:
            columns = ['date', '利息收入', '利息支出', '净利息收入', '坏账准备金', '扣除坏账准备金的净利息收入', \
            '非利息收入', '非利息支出', '营业利润', '营业外收支净额', '非经常性损益', '利润总额（税前）', \
            '所得税', '未合并的子公司利润', '其他调整', '合并净利润', '少数股东损益', '归属于母公司的净利润', \
            '优先股股息', '归属于普通股东的综合收益', '普通股本', '基本每股收益', '本期每股红利']
        df = pd.DataFrame(tt, )
        df['code'] = sym
        # print(df)        
        records = json.loads(df.T.to_json()).values()
        us_income.insert(records)
        print(sym,' income table crawled.')
        time.sleep(3)

def fetchCash(sym, quarter = True):  
    """crawled to TRMB"""
    if quarter: 
        url = 'http://quotes.money.163.com/usstock/' + str(sym) + '_cash.html?type=quarter'
    else:
        url = 'http://quotes.money.163.com/usstock/' + str(sym) + '_cash.html'
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
        if len(table) < 2:
            if not url.endswith('quarter'):
                return
            return fetchIndicators(sym,False)

        tt = np.array(table)
        tt=tt.transpose()
        if len(tt[0]) == 23:
            columns = ['date','经营产生的现金流入','净利润（现金流表）', '折旧摊销和损耗', '递延税和投资税优惠', \
                '非现金项目' , '非经常项目损益', '营运资本变动', '经营净现金流', '资本性支出', \
                '并购资产净额', '固定资产和业务出售收入', '投资买卖净额', '投资净现金流', '红利支付', \
                '股权融资净额', '债权融资净额', '其他融资净额', '融资净现金流', '汇率变动影响', '其他现金流', \
                '净现金流', '自由现金流']
        else:
            columns = ['date','经营产生的现金流入','非经常项目损益', '营运资本变动', '经营净现金流', '资本性支出', \
                '并购资产净额', '固定资产和业务出售收入', '投资买卖净额', '投资净现金流', '红利支付', \
                '股权融资净额', '债权融资净额', '其他融资净额', '融资净现金流', '汇率变动影响', '其他现金流', \
                '净现金流', '自由现金流']
        
        df = pd.DataFrame(tt, columns=columns)
        df['code'] = sym
        records = json.loads(df.T.to_json()).values()
        us_cash.insert(records)
        print(sym,' cash table crawl.')
        time.sleep(3)


if __name__ == '__main__':
    valid_once = True
    for tid in range(len(T)):
        sym = T.iloc[tid].symbol        
        if valid_once and sym != 'CLR':  
            print(sym ,' has crawled.')          
            continue
                   
        fetchCash(sym) 
        fetchIncome(sym)
        fetchBalance(sym) 
        # exit()          
        valid_once = False

