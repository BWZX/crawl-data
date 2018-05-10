import urllib, urllib.request
from pymongo import MongoClient
from pyquery import PyQuery as pq
from pandas import DataFrame as dtf
import json
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
        data_table = {}
        table = d('table#FundHoldSharesTable')
        for tr in table('tr').items():
            print(tr('td').text()+' then:\n')
            if not tr('td').eq(3):
                date = tr('td').eq(1).text()
                data_table[date] = []
                # print(date)
            if not tr('td').eq(1).text().isnumeric():
                continue
            cell = []
            for td in tr('td').items():
                cell.append(td.text()) 
                # print(cell)

            data_table[date].append(cell.copy())
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


if __name__ == '__main__':
    # fetchType(0)  
    # fetchHoldFund('002458')

    # print(fetchSummary('002458'))
    # exit()

    for code in config.stolist:
        print(code)
        finance_sumery = fetchSummary(code)    
        # print('\n\n')
        start_year = min(finance_sumery).split('-')[0]
        end_year = max(finance_sumery).split('-')[0]
        finance_detail = {}
        for year in range(int(start_year),int(end_year)+1):
            data = fetchCashFlow(code, year)
            data.append(fetchProfit(code, year))
            datadate = data[0]
            tidydata = {}
            for ss,v in enumerate(datadate[1:]):
                tidydata[v] = []
                for dt in data[1:]:
                    cell = []
                    cell.append(dt[0])
                    cell.append(dt[ss+1])
                    tidydata[v].append(cell.copy())        
            finance_detail.update(tidydata)

        # print(tidydata)
        finance = []
        for it in finance_detail:
            temp = finance_detail[it] + finance_sumery[it]
            temp = [['date', it]] + temp
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
            df.loc[len(df)] = row.copy()

        df['code'] = code
        # print(df)
        records = json.loads(df.T.to_json()).values()
        financetable.insert(records)
    
    
    
    # fetchStockStructure('002458')

