#!/usr/bin/python
# -*- coding: utf-8 -*-

import config
import json


def insertList(data):    
    url='http://10.8.0.5:4242/api/put'

    print(data)

    pass

'''
async def fetchData(url):
    conn = aiohttp.TCPConnector(limit=config.REQ_AMOUNTS)    
    s = aiohttp.ClientSession(headers = config.HEADERS, connector=conn)
    
    dat = {
        "metric": "test.t1",
        "timestamp": 1346846405,
        "value": 34,
        "tags": {
           "host": "web01",
           "dc": "lgs"
        }
    }

    # print(da.value)
    async with s.post(url, data=json.dumps(dat)) as r:    
        txt = await r.text(encoding='utf-8')
        print(r.status)
        print(txt)
        # await callback(data, s)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    url='http://10.8.0.5:4242/api/put'
    #coroutine in tasks will run 
    tasks = [fetchData(url)]  
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close() 
'''
