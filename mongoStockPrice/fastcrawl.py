import json
import sys
sys.path.append('../publicstuff')
import tushare as ts
import config
import pymongo
from pymongo import MongoClient
client = MongoClient('mongodb://node0:27017')
security = client.quantDay.security

def fetchAll(slist):    
    """
        获取所有的股票的历史数据，
        不包括成交明细，同时把数据存到数据库。
        这个函数应该只运行一次        
    """
    for sto in slist:
        print(sto)        
        df_D=ts.get_k_data(sto,'1980-01-01',ktype='D') 
        df_D['name']=config.StocksList[sto]
        records = json.loads(df_D.T.to_json()).values()
        security.insert(records)

if __name__ == '__main__':
    fetchAll(config.stolist)
