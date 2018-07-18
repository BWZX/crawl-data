import urllib, urllib.request
from pymongo import MongoClient
from pyquery import PyQuery as pq
from pandas import DataFrame as dtf
import json
import numpy as np
from mongoconnect import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)),'../publicstuff'))
import config

"""
type: http://vip.stock.finance.sina.com.cn/corp/go.php/vCI_CorpOtherInfo/stockid/002458/menu_num/2.phtml
finance: http://money.finance.sina.com.cn/corp/go.php/vFD_FinanceSummary/stockid/002458.phtml
predict: http://money.finance.sina.com.cn/corp/go.php/vFD_AchievementNotice/stockid/002458.phtml
fund: http://vip.stock.finance.sina.com.cn/corp/go.php/vCI_FundStockHolder/stockid/002458.phtml
"""       

def fetchType(code):
    url = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vCI_CorpOtherInfo/stockid/002458/menu_num/2.phtml'
    request=urllib.request.Request(url)  
    result=urllib.request.urlopen(request, timeout=25)
    if result.code == 200 or 204:
        ts = result.read()
        ts=ts.decode('gbk')
        # print(ts)
        d = pq(ts)
        clas = d('table.comInfo1 tr').eq(2)
        hy = clas('td').eq(0).text()
        print(hy)
        gn=[]
        table = d('table.comInfo1').eq(1)
        for it in table('tr').items():
            gn.append(it('td').eq(0).text())
        gn = gn[2:]        
        print(gn)       
    else:
        raise Exception('crawl failure!')

def fetchCashFlow(code, year):
    url = 'http://money.finance.sina.com.cn/corp/go.php/vFD_CashFlow/stockid/' + code +'/ctrl/'+ str(year) +'/displaytype/4.phtml'
    request=urllib.request.Request(url)  
    result=urllib.request.urlopen(request, timeout=25)
    if result.code == 200 or 204:
        ts = result.read()
        ts=ts.decode('gbk')
        # print(ts)
        d = pq(ts)
        table = d('table#ProfitStatementNewTable0 tbody')
        data_table = []
        data_table.append([])
        for it in table('tr').eq(0)('td').items():  #date
            data_table[-1].append(it.text())
       
        data_table.append([])
        for it in table('tr').eq(6)('td').items():  #op cash income
            data_table[-1].append(it.text())

        data_table.append([])
        for it in table('tr').eq(12)('td').items():  #net op cash
            data_table[-1].append(it.text())

        data_table.append([])
        for it in table('tr').eq(25)('td').items():  #net invest cash
            data_table[-1].append(it.text())

        data_table.append([])
        for it in table('tr').eq(34)('td').items():  #interest payment
            data_table[-1].append(it.text())

        data_table.append([])
        for it in table('tr').eq(38)('td').items():  #net raise cash
            data_table[-1].append(it.text())

        data_table.append([])
        for it in table('tr').eq(48)('td').items():  #fixed assets deprecition
            data_table[-1].append(it.text())

        data_table.append([])
        for it in table('tr').eq(49)('td').items():  #amortization of intangible assets
            data_table[-1].append(it.text())

        data_table.append([])
        for it in table('tr').eq(50)('td').items():  #long-term unamortized expenses
            data_table[-1].append(it.text())

        # print(data_table)  
        return data_table    
    else:
        raise Exception('crawl failure!')
    pass

def fetchProfit(code, year):
    url = 'http://money.finance.sina.com.cn/corp/go.php/vFD_ProfitStatement/stockid/'+ code +'/ctrl/'+ str(year) +'/displaytype/4.phtml'
    request=urllib.request.Request(url)  
    result=urllib.request.urlopen(request, timeout=25)
    if result.code == 200 or 204:
        ts = result.read()
        ts = ts.decode('gbk')
        # print(ts)
        d = pq(ts)
        table = d('table#ProfitStatementNewTable0 tbody')
        cell = []
        for it in table('tr').eq(19)('td').items():
            cell.append(it.text())
        
        # print(cell)
        return cell
    else:
        raise Exception('crawl failure!')

def fetchHoldFund(stoid):
    url = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vCI_FundStockHolder/stockid/' + stoid + '.phtml'
    request=urllib.request.Request(url)  
    result=urllib.request.urlopen(request, timeout=25)
    if result.code == 200 or 204:
        ts = result.read()
        ts=ts.decode('gbk')
        # print(ts)
        d = pq(ts)
        data_table = []
        table = d('table#FundHoldSharesTable')
        for tr in table('tr').items():
            # print(tr('td').text()+' then:\n')
            if not tr('td').eq(3):
                date = tr('td').eq(1).text()                
                # print(date)
            if not tr('td').eq(1).text().isnumeric():
                continue
            cell = []
            cell.append(date)            
            for td in tr('td').items():
                cell.append(td.text())                 
                # print(cell)
            if len(cell) == 7:
                data_table.append(cell.copy())
        return data_table
    else:
        raise Exception('crawl failure!')

def fetchSummary(stoid):
    url = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vFD_FinanceSummary/stockid/' + stoid + '.phtml'
    request=urllib.request.Request(url)  
    result=urllib.request.urlopen(request, timeout=25)
    if result.code == 200 or 204:
        ts = result.read()
        ts=ts.decode('gbk')
        # print(ts)
        d = pq(ts)
        data_table = {}
        table = d('table#FundHoldSharesTable')
        setdate = True
        for tr in table('tr').items():            
            if not tr('td') or not tr('td').text():
                # print('none')
                continue
            # print(tr.text()+' then:\n')
            if setdate:
                date = tr('td').eq(1).text()
                data_table[date] = []
                setdate = False
                # print(date)
                continue            
            cell = []
            title = tr('td').eq(0).text()
            if title == '固定资产合计':
                continue
            cell.append(title)
            txt = tr('td').eq(1).text()
            txt = txt[:-1]
            txt = txt.replace(',','')
            cell.append(txt) 
            # print(cell)
            data_table[date].append(cell.copy())
            if title == '净利润':
                setdate = True
        # print(data_table)
        return data_table
    else:
        raise Exception('crawl failure!')

def fetchStockStructure(stoid):
    url = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vCI_StockStructure/stockid/' + stoid + '.phtml'
    request=urllib.request.Request(url)  
    result=urllib.request.urlopen(request, timeout=25)
    if result.code == 200 or 204:
        ts = result.read()
        ts=ts.decode('gbk')
        # print(ts)
        d = pq(ts)
        data_table = []
        for i in range(1000):
            table = d('table#StockStructureNewTable'+str(i))
            if not table:
                break
            table = table('tbody')
            cell = []
            for td in table('tr').eq(0)('td').items():  
                txt = td.text().split(' ')[0]
                cell.append(txt)
            data_table.append(cell.copy())
            cell = []
            for td in table('tr').eq(1)('td').items():
                txt = td.text().split(' ')[0]
                cell.append(txt)
            data_table.append(cell.copy())
            cell = []
            for td in table('tr').eq(4)('td').items():
                txt = td.text().split(' ')[0]
                cell.append(txt)
            data_table.append(cell.copy())
            cell = []
            for td in table('tr').eq(6)('td').items():
                txt = td.text().split(' ')[0]
                cell.append(txt)
            data_table.append(cell.copy())
            cell = []
            for td in table('tr').eq(7)('td').items():
                txt = td.text().split(' ')[0]
                cell.append(txt)
            data_table.append(cell.copy())
            cell = []
            for td in table('tr').eq(8)('td').items():
                txt = td.text().split(' ')[0]
                cell.append(txt)
            data_table.append(cell.copy())
        return data_table
    else:
        raise Exception('crawl failure!')

def Finance_Main():
    import time
    # fetchType(0)  
    # fetchHoldFund('002458')

    # print(fetchSummary('002458'))
    # exit()
    def drop_except(code):
        try:
            summe = fetchSummary(code)  
            if not summe:
                time.sleep(10)
                drop_except(code)
            else:
                return summe
            pass
        except Exception:
            time.sleep(3)
            drop_except(code) 
            pass

    indexxx = config.stolist.index('601789') +1
    for code in config.stolist[indexxx:]:    #['000422']:  #422
        print(code)
        time.sleep(3)
        finance_sumery = drop_except(code)  
        # print('\n\n')
        start_year = min(finance_sumery).split('-')[0]
        end_year = max(finance_sumery).split('-')[0]
        finance_detail = {}
        for year in range(int(start_year),int(end_year)+1):
            data = fetchCashFlow(code, year)
            data.append(fetchProfit(code, year))
            # print(data)
            datadate = data[0]
            tidydata = {}
            for ss,v in enumerate(datadate[1:]):
                tidydata[v] = []
                for dt in data[1:]:
                    cell = []
                    if len(dt)==0:
                        continue
                    cell.append(dt[0])
                    if len(dt) > (ss+1):
                        cell.append(dt[ss+1])
                    else:
                        cell.append('--')
                    tidydata[v].append(cell.copy())        
            finance_detail.update(tidydata)

            # print(tidydata)
        finance = []
        for it in finance_detail:
            if finance_detail.get(it) and finance_sumery.get(it) :
                temp = finance_detail[it] + finance_sumery[it]
            else:
                continue
            temp = [['date', it]] + temp
            # print(temp)
            finance.append(temp)

        # print(finance)

        columns =['date', 'op_income', 'net_op_cf', 'net_invest_cf', 'pay_intest',\
            'net_raise_cf', 'depreciation', 'amortization', 'long_term_amortization', 'total_profit',\
            'net_asset_ps', 'eps', 'cf_ps', 'accumulation_ps', 'total_float_assets', 'total_assets',\
            'long_term_debt', 'main_op_income', 'finance_fee', 'net_profit']
        df = dtf([],columns=columns)

        for it in finance:
            row = []   # each row will be a dataframe's row.
            rown = []
            for tt in it:
                rown.append(tt[0])
                row.append(tt[1])
            # print(row)
            # print(rown)
            # print(columns)
            if len(row) == len(columns):
                df.loc[len(df)] = row.copy()
            else:
               continue
            

        df['code'] = code
        # print(df)
        records = json.loads(df.T.to_json()).values()
        financetable.insert(records)
  

if __name__ == '__main__': 
    import time
    for code in config.stolist:
        print(code)
        hfund = fetchHoldFund(code)
        hfund_dtf = dtf(hfund,columns=['date','fund_name','fund_code','hold_shares','liquid_share_rate','maket_value','net_value_rate'])
        hfund_dtf['code'] = code
        # print(hfund_dtf)
        # exit()        
        # print(df)
        records = json.loads(hfund_dtf.T.to_json()).values()
        holdfund.insert(records)
        # struct_data = fetchStockStructure(code)    
        # ff = dtf(struct_data)  
        # del ff[0]   
        # dd = ff.T
        # dd = dd.as_matrix()
        # shape = dd.shape
        # rows = shape[0] * (shape[1]/6)
        # dd = dd.reshape(int(rows), 6)
        # columns_name = ['action_date','report_date','general_equity','flow_equity','executive_equity','restrict_equity']
        # df = dtf(dd,columns=columns_name)
        # df['code'] = code
        # records = json.loads(df.T.to_json()).values()
        # equitystructure.insert(records)
        # time.sleep(5)