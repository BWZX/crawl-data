from mongoModel import *


sec=Securities.objects.get({'code':'000001'})
ShareBonus(sec).save()
ShareRation(sec).save()
# Finance(sec,'').save()
print(sec)
# for obj in Securities.objects.all():    
#     print(obj.industry)

