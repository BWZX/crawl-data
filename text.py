import json
import urllib, urllib.request
from multiprocessing import Pool
import os, time
import tushare as ts
import config

# url='http://10.8.0.5:4242/api/put'
# data=[{
#         "metric": "test.t1",
#         "timestamp": 1346846405,
#         "value": 354,
#         "tags": {
#            "host": "web01",
#            "dc": "lds"
#         }
#     },{
#         "metric": "test.t1",
#         "timestamp": 1356846400,
#         "value": 34,
#         "tags": {
#            "host": "web01",
#            "dc": "lds"
#         }
#     }]
# data = json.dumps(data)  
# data=bytes(data,'utf8')  
# request=urllib.request.Request(url)  
# result=urllib.request.urlopen(request,data)
# print(result.getcode())  
def getSto(code):
    print(99999)
    df=ts.get_k_data(code)
    return {'data':df ,'code':code} 

if __name__ == '__main__':
  p=Pool(5)
  dd={}


  def ins(da):
    print(da['data'])    
    pass

  for i in config.stolist[0:5]:
    p.apply_async(getSto, args=(i,), callback=ins )

  for i in config.stolist[5:10]:
    p.apply_async(getSto, args=(i,), callback=ins )
    print(9)

  p.close()
  p.join()
  # print(dd[7])