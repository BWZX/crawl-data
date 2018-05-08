import urllib, urllib.request
from pymongo import MongoClient
from pyquery import PyQuery as pq
from pandas import DataFrame as dtf
__client = MongoClient('mongodb://admin:%2B@node0:27017')
future = __client.quantDay.future
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
        print('request faild.') 

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
        data_table = {}
        data_table['date'] = []
        for it in table('tr').eq(0)('td').items():  #date
            data_table['date'].append(it.text())
       
        data_table['opincome'] = []
        for it in table('tr').eq(6)('td').items():  #op cash income
            data_table['opincome'].append(it.text())

        data_table['netopc'] = []
        for it in table('tr').eq(12)('td').items():  #net op cash
            data_table['netopc'].append(it.text())

        data_table['netic'] = []
        for it in table('tr').eq(25)('td').items():  #net invest cash
            data_table['netic'].append(it.text())

        data_table['ip'] = []
        for it in table('tr').eq(34)('td').items():  #interest payment
            data_table['ip'].append(it.text())

        data_table['netrc'] = []
        for it in table('tr').eq(38)('td').items():  #net raise cash
            data_table['netrc'].append(it.text())

        data_table['fad'] = []
        for it in table('tr').eq(48)('td').items():  #fixed assets deprecition
            data_table['fad'].append(it.text())

        data_table['aoia'] = []
        for it in table('tr').eq(49)('td').items():  #amortization of intangible assets
            data_table['aoia'].append(it.text())

        data_table['ltue'] = []
        for it in table('tr').eq(50)('td').items():  #long-term unamortized expenses
            data_table['ltue'].append(it.text())

        print(data_table)        
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
        
        print(cell)



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
        print(data_table)

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
            print(tr('td').text()+' then:\n')
            if not tr('td').eq(1).text():
                print('none')
                continue
            if setdate:
                date = tr('td').eq(1).text()
                data_table[date] = []
                setdate = False
                print(date)
                continue            
            cell = []
            title = tr('td').eq(0).text()
            cell.append(title)
            txt = tr('td').eq(1).text()
            txt = txt[:-1]
            txt = txt.replace(',','')
            cell.append(txt) 
            print(cell)
            data_table[date].append(cell.copy())
            if title == '净利润':
                setdate = True
        print(data_table)

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
        print(data_table)


if __name__ == '__main__':
    # fetchType(0)  
    # fetchHoldFund('002458')
    # fetchCashFlow('002458', 2017)
    # fetchProfit('002458', 2017)
    fetchStockStructure('002458')

