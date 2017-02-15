import json
import urllib, urllib.request

url='http://10.8.0.5:4242/api/put'
data=[{
        "metric": "test.t1",
        "timestamp": 1346846405,
        "value": 354,
        "tags": {
           "host": "web01",
           "dc": "lds"
        }
    },{
        "metric": "test.t1",
        "timestamp": 1356846400,
        "value": 34,
        "tags": {
           "host": "web01",
           "dc": "lds"
        }
    }]
data = json.dumps(data)  
data=bytes(data,'utf8')  
request=urllib.request.Request(url)  
result=urllib.request.urlopen(request,data)
print(result.getcode())  