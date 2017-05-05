#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    this file is used to control the data crawling
"""
import collectData
import config
import time
import json
from datetime import datetime as dt

if __name__ == '__main__':
    """
        如果是第一次运行，那么先执行collectData.py文件
    """    
    while True:
        collectData.fetchAllStocksTodayTickData()
        time.sleep(config.AppConfig['data_updata_interval'])

        with open('mongo.json','w') as f:
            f.write(json.dumps(collectData.MongodbJson))

        now=dt.now()
        if now.hour==18 and now.minute<=5:
            collectData.fetchAllStocksTodayNotTickData()
        pass
    