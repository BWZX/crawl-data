# Create your models here.

from pymongo import TEXT
from pymongo.operations import IndexModel
from pymodm import connect, fields, MongoModel, EmbeddedMongoModel
from datetime import datetime as dt, timedelta as td


# from securities.models import Security


# Connect to MongoDB first. PyMODM supports all URI options supported by
# PyMongo. Make sure also to specify a database in the connection string:
connect('mongodb://node0:27017/quantDay')

class security(MongoModel):
    date = fields.CharField()    
    open = fields.FloatField()
    close = fields.FloatField()
    high = fields.FloatField()
    low = fields.FloatField()    
    volume = fields.FloatField()
    code = fields.CharField()
    name = fields.CharField()    

# import pymongo
# from pymongo import MongoClient
# client = MongoClient('mongodb://node0:27017')
# db = client.quantDay
# security=db.securities


if __name__ == '__main__':
    # ss={
    #     'date': dt(2015,4,5),
    #     'open':1.11,
    #     'close': 1.22,
    #     'high': 1.33,
    #     'low': 1.21,
    #     'volume':214.3,
    #     'code':'0901'
    # }
    # security.insert_one(ss)
    # security('2001123').save()
    # ll=list(security.objects.raw({'date':dt(2015,4,5), 'code':'001'}))
    # print(ll)
    # security.objects.raw({'code':'099'}).update({'$set':{'name': '0o9','open':832}})
    # print('sjkg')
    for item in security.objects.all():
        print(item.date,'skjg')