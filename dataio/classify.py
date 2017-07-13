"""
this file help to fill the database table, such as Classified
hs300 sz50 zz500
"""
import sys
sys.path.append('../publicstuff')
import tushare as ts 
import pandas as pd
import config
from mongoModel import *


industry = ts.get_industry_classified()
concept = ts.get_concept_classified()
area = ts.get_area_classified()
hs300 = ts.get_hs300s()
sz50 = ts.get_sz50s()
zz500= ts.get_zz500s()

res = pd.merge(area, industry, on=['code','name'])
res = pd.merge(res, concept, on=['code','name'])
print(res)
# exit()

for stock in config.stolist:
    current = res[res.code==stock]
    name = config.StocksList[stock]
    area_ = current.iloc[0,2]
    inds = list(set(list(current.c_name_x)))
    conc = list(set(list(current.c_name_y)))
    Classified(stock,name,inds,conc,area_).save()

for hs in hs300.iterrows():
    Hs300(hs[1]['code'], hs[1]['name']).save()

for sz in sz50.iterrows():
    Sz50(sz[1]['code'], sz[1]['name']).save()

for zz in zz500.iterrows():
    Zz500(zz[1]['code'], zz[1]['name']).save()


