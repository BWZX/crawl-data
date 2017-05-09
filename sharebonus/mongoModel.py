# Create your models here.

from pymongo import TEXT
from pymongo.operations import IndexModel
from pymodm import connect, fields, MongoModel, EmbeddedMongoModel


# from securities.models import Security


# Connect to MongoDB first. PyMODM supports all URI options supported by
# PyMongo. Make sure also to specify a database in the connection string:
connect('mongodb://127.0.0.1:27017/quant')

class Exchange(MongoModel):
    name = fields.CharField()

class Securities(MongoModel):
    name = fields.CharField()
    code = fields.CharField()
    exchange_id = fields.ReferenceField(Exchange)
    industry = fields.CharField()

class PriceEvent(MongoModel):
    security_id = fields.ReferenceField(Securities)
    event_type = fields.IntegerField()
    change_at = fields.IntegerField()
    price_before = fields.FloatField()
    price_after = fields.FloatField()
    ratio = fields.FloatField()

class TimeSeries(MongoModel):
    security = fields.ReferenceField(Securities)
    metric = fields.CharField()
    tag = fields.CharField()
    start_at = fields.IntegerField()
    end_at = fields.IntegerField()

class ShareBonus(MongoModel):
    gupiao = fields.ReferenceField(Securities)
    gonggaori = fields.CharField()
    chuquanchuxiri = fields.CharField()
    dengjiri = fields.CharField()
    songgu = fields.FloatField()
    zhuanzeng = fields.FloatField()
    paixi = fields.FloatField()
    jingdu = fields.CharField()

class ShareRation(MongoModel):
    gupiao = fields.ReferenceField(Securities)
    gonggaori = fields.CharField()
    shangshiri = fields.CharField()
    chuquanri = fields.CharField()
    dengjiri = fields.CharField()
    peigufangan = fields.FloatField()
    peigujiage = fields.FloatField()    
    jizhunguben = fields.FloatField()
    
    shijipeigushu = fields.FloatField()
    shijipeigubili = fields.FloatField()

    

if __name__ == '__main__':
    # exchange = Exchange.objects.get({'name':'沪深股市'})
    # Exchange(name='沪深股市').save()
    # exchange=Exchange.objects.raw({'name':'沪深股市'}).all()[0]._id
    # print(exchange)
    # Securities('test','test',exchange).save()
    
    
    for obj in Securities.objects.all():
        print(obj.name)
