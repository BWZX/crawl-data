import sys
sys.path.append('../publicstuff')
import aiohttp
import asyncio
import processData as pd
from mongoModel import *
import config


stolist=config.stolist
try:
    with open('thisprogress.ini','r') as f:
        now_at=f.read()
        print("now_at ",now_at)
        stolist=stolist[stolist.index(now_at)+1:]
except Exception:
    pass

@asyncio.coroutine
def fetchData(session=None, callback = pd.processData):
    #set request url and parameters here or you can pass from outside. 
    
    #use s.** request a webside will keep-alive the connection automaticaly,
    #so you can set multi request here without close the connection 
    #while in the same domain.
    #i.e. 
    #yield from s.get('***/page1')
    #yield from s.get('***/page2')
    f=open('debug.log','a')
    ######################################################################## 
    cookies = {
        
    }

    conn = aiohttp.TCPConnector(limit=config.REQ_AMOUNTS)    
    s = aiohttp.ClientSession(headers = config.HEADERS, cookies=cookies, connector=conn)   

    url = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vISSUE_ShareBonus/stockid/'
    r='text'
    index=0
    length=len(stolist)
    while index<length:                
        coroutines = []        
        for i in range(10):
            if index>=length:
                break;
            coroutines.append(s.get(url+stolist[index]+'.phtml'))
            index=index+1

        for coroutine in asyncio.as_completed(coroutines):             
            try:
                r = yield from coroutine
            except Exception:
                # yield from asyncio.sleep(2)
                r = yield from coroutine
            if not r:
                continue
            try:
                data = yield from r.text(encoding='gb2312')
            except UnicodeDecodeError:
                try:
                    data = yield from r.text(encoding='utf-8')
                except UnicodeDecodeError:
                    f.write(str(stolist[index])+' nearby has a page cannot be parsed.\n')
                    continue
            data = yield from callback(s, data)
            # print(data)

            try:
                # print(data['shareCode'])
                sec=Securities.objects.get({'code':data['shareCode']})
            except Securities.DoesNotExist:
                # print("the share code isn't save yet, is odd.")
                # exit()
                exc=Exchange.objects.get({'name':'沪深股市'})
                sec=Securities(config.StocksList[data['shareCode']], data['shareCode'], exc).save()

            try:
                # pass
                print(data['shareBonus'][0]['gonggaori'],' and ',sec._id)
                bns = ShareBonus.objects.get({'gupiao':sec._id, 'gonggaori': data['shareBonus'][0]['gonggaori']})
            except ShareBonus.DoesNotExist:
                for item in data['shareBonus']:
                    item['gupiao']=sec
                    ShareBonus(item['gupiao'], item['gonggaori'], item['chuquanchuxiri'], item['dengjiri'], item['songgu'], item['zhuanzeng'], item['paixi'], item['jingdu']).save()
                for item in data['rationBonus']:
                    item['gupiao']=sec
                    ShareRation(item['gupiao'], item['gonggaori'], item['shangshiri'], item['chuquanri'], item['dengjiri'], item['peigufangan'], item['peigujiage'], item['jizhunguben'], item['shijipeigushu'], item['shijipeigubili']).save()
        print('rough complete.')
        with open('thisprogress.ini','w') as pr:
            pr.write(str(data['shareCode']))

    f.close()
        # yield from asyncio.sleep(1)
################################################################
################################################################

if __name__ == '__main__':    
    loop = asyncio.get_event_loop()    
    # tasks = []    
    loop.run_until_complete(fetchData(pd.processData))
    loop.close() 
 