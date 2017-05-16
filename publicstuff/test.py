from mongoModel import *

sec=Securities.objects.get({'code':'000001'})
ShareBonus(sec).save()
ShareRation(sec).save()
# Finance(sec,'').save()

for obj in Finance.objects.all():    
    print(obj.time)

Finance.objects.raw({ 'time' : 'jj'}).update(
{ '$set' : { 'time' : 'yyyj'}})

for obj in Finance.objects.all():    
    print(obj.time)

# f=open('debug.log','a')
# f.write('sss')
# f.close()