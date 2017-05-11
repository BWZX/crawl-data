import aiohttp
import asyncio
import config
import processData as pd
import sys
sys.path.append('../publicstuff')
from mongoModel import *

@asyncio.coroutine
def fetchData(session=None, callback = pd.processData):
    #set request url and parameters here or you can pass from outside. 
    
    #use s.** request a webside will keep-alive the connection automaticaly,
    #so you can set multi request here without close the connection 
    #while in the same domain.
    #i.e. 
    #yield from s.get('***/page1')
    #yield from s.get('***/page2')
    ######################################################################## 
    cookies = {
        
    }

    conn = aiohttp.TCPConnector(limit=config.REQ_AMOUNTS)    
    s = aiohttp.ClientSession(headers = config.HEADERS, cookies=cookies, connector=conn)   

    url = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vISSUE_ShareBonus/stockid/'
    r='text'
    index=0
    length=len(config.stolist)
    while index<length:                
        coroutines = []        
        for i in range(10):
            if index>=length:
                break;
            coroutines.append(s.get(url+config.stolist[index]+'.phtml'))
            index=index+1

        for coroutine in asyncio.as_completed(coroutines):             
            try:
                r = yield from coroutine
            except Exception:
                # yield from asyncio.sleep(2)
                r = yield from coroutine
            if not r:
                continue
            data = yield from r.text(encoding='gb2312')
            data = yield from callback(s, data)

            try:
                print(data['shareCode'])
                sec=Securities.objects.get({'code':data['shareCode']})
            except Securities.DoesNotExist:
                print("the share code isn't save yet, is odd.")
                exit()

            try:
                bns = ShareBonus.objects.get({'gupiao':sec, 'gonggaori': data['shareBonus'][0]['gonggaori']})
            except ShareBonus.DoesNotExist:
                for item in data['ShareBonus']:
                    item['gupiao']=sec
                    ShareBonus(item['gupiao'], item['gonggaori'], item['chuquanchuxiri'], item['dengjiri'], item['songgu'], item['zhuanzeng'], item['paixi'], item['jingdu']).save()
                for item in data['shareRation']:
                    item['gupiao']=sec
                    ShareRation(item['gupiao'], item['gonggaori'], item['shangshiri'], item['chuquanri'], item['dengjiri'], item['peigufangan'], item['peigujiage'], item['jizhunguben'], item['shijipeigushu'], item['shijipeigubili']).save()

        # yield from asyncio.sleep(1)
        

################################################################
################################################################

    

if __name__ == '__main__':    
    loop = asyncio.get_event_loop()    
    # tasks = []    
    loop.run_until_complete(fetchData(pd.processData))
    loop.close() 
 