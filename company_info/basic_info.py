import urllib, urllib.request
from pymongo import MongoClient
__client = MongoClient('mongodb://admin:%2B@node0:27017')
future = __client.quantDay.future

"""
type: http://vip.stock.finance.sina.com.cn/corp/go.php/vCI_CorpOtherInfo/stockid/002458/menu_num/2.phtml
finance: http://money.finance.sina.com.cn/corp/go.php/vFD_FinanceSummary/stockid/002458.phtml
predict: http://money.finance.sina.com.cn/corp/go.php/vFD_AchievementNotice/stockid/002458.phtml
fund: http://vip.stock.finance.sina.com.cn/corp/go.php/vCI_FundStockHolder/stockid/002458.phtml
"""


def fetchData(arg):
    url = ''
    request=urllib.request.Request(url)  
    result=urllib.request.urlopen(request, timeout=25)
    if result.code == 200 or 204:
        s 
    else:
        print('request faild.')    
if __name__ == '__main__':
    fetchData('V0')  

