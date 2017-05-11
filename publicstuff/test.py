from mongoModel import *

for obj in Securities.objects.all():
    print(obj.name)
