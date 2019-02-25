import aiohttp
import asyncio

def Bb():
    dd={'a':9}
    Aa(dd)
    print(dd['a'])
def Aa(ff):
    ff['a']=9999
    pass

# @asyncio.coroutine
# def fetchData(session=None):
    
#     conn = aiohttp.TCPConnector()    
#     s = aiohttp.ClientSession(connector=conn) 
                 
#     coroutines = []        
    
#     coroutines.append(s.get('www.baidu.com'))
#     coroutines.append(s.get('www.hao123.com'))
    

#     for coroutine in asyncio.as_completed(coroutines): 
#         print(dir(coroutine),'\n\n',coroutine.__str__)            
#         try:
#             r = yield from coroutine
#         except Exception:
#             pass
#股票除权后的昨天收盘参考价格=(股票除权前昨天的收盘价格-每股现金分红+每股配股比例*配股价格)/(1+每股转增比例+每股送股比例+每股配股比例)。

if __name__ == '__main__':    
    # loop = asyncio.get_event_loop()    
    # # tasks = []    
    # loop.run_until_complete(fetchData())
    # loop.close() 
    Bb()
