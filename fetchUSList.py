import urllib.request

name="name"
cname="cname"
category="category"
symbol="symbol"
price="price"
diff="diff"
chg="chg"
preclose="preclose"
high="high"
low="low"
amplitude="amplitude"
volume="volume"
mktcap="mktcap"
pe="pe"
market="market"
category_id="category_id"
null = 'null'
kk = 'jjj'
f = open('usall.csv','w',encoding='utf8')
ss='symbol,name,cname,category,mktcap,market,pe'
f.write(ss+'\n')
open="open"
for page in range(148):
    url = "http://stock.finance.sina.com.cn/usstock/api/jsonp.php/IO.XSRV2.CallbackList['f0j3ltzVzdo2Fo4p']/US_CategoryService.getList?num=60&sort=&asc=0&market=&id=&page="
    url = url + str(page+1)
    request=urllib.request.Request(url)  
    result=urllib.request.urlopen(request, timeout=25)
    if result.code == 200 or 204:
        ts = result.read()
        ts=ts.decode('gbk')
        # import pdb;pdb.set_trace()
        ts = ts[62:-4]
        ts = 'kk = '+ts
        # print(ts)
        exec(ts)        
        # print(kk)
        for it in kk:
            ss=''+it[symbol]+','+it[name].replace(',',' ')+','+it[cname].replace(',',' ')+','+it[category].replace(',',' ')+','+it[mktcap]+','+it[market]+','+it[pe]
            ss = ss.replace('\n',' ')
            ss = ss.replace('\r',' ')
            # if it[symbol] == 'BSE':
            #     import pdb;pdb.set_trace()
            f.write(ss+'\n')            

f.close()

 
# if __name__ == '__main__':
    # main(1)