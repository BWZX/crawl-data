# -*- coding: utf8 -*-

from mongoModel import *

# sec=Securities.objects.get({'code':'000001'})
# ShareBonus(sec).save()
# ShareRation(sec).save()
# # Finance(sec,'').save()

# for obj in Finance.objects.all():    
#     print(obj.time)

# Finance.objects.raw({ 'time' : 'jj'}).update(
# { '$set' : { 'time' : 'yyyj'}})

# for obj in Finance.objects.all():    
#     print(obj.time)
import json
# f=open('../mongoStockPrice/stocklist.json','r')
# sto=json.loads(f.read())
# f.close()
# stocks=list(sto.keys())
# stocks.sort()
# print(stocks)
# print(stocks.index('000408'))
import os,sys
print(__file__)