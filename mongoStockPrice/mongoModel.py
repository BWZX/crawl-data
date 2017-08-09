# Create your models here.

from pymongo import TEXT
from pymongo.operations import IndexModel
from pymodm import connect, fields, MongoModel, EmbeddedMongoModel


# from securities.models import Security


# Connect to MongoDB first. PyMODM supports all URI options supported by
# PyMongo. Make sure also to specify a database in the connection string:
connect('mongodb://node0:27017/quantDay')

class security(MongoModel):
    date = fields.DateTimeField()    
    open = fields.FloatField()
    close = fields.FloatField()
    high = fields.FloatField()
    low = fields.FloatField()    
    volume = fields.FloatField()
    code = fields.CharField()
    name = fields.CharField()    
    period = fields.CharField()


if __name__ == '__main__':
    for item in security.objects.all():
            print(item.code)