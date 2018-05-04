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

def fetch3Table(code, tb, year):
    pass

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

if __name__ == '__main__':
    # fetchType(0)  
    fetchHoldFund('002458')

