import asyncio
from pyquery import PyQuery as pq
import config

def Float(a=''):
    if not a:
        return 0.0
    a=a.replace('-','')
    a=a.replace(',','')
    if not a:
        a='0'
    return float(a)


@asyncio.coroutine
def processData(s, data):
    '''
    data is from the http response in main module.
    '''
    d = pq(data)
    maintable=d('table#sharebonus_1 tbody')
    sharecode=d('div.tbtb01 h2').text()[1:].strip()

    shareBonus=[]
    for item in maintable('tr').items():
        bonus={}
        bonus['gonggaori'] = item('td').eq(0).text()
        bonus['songgu'] = Float(item('td').eq(1).text())
        bonus['zhuanzeng'] = Float(item('td').eq(2).text())
        bonus['paixi'] = Float(item('td').eq(3).text())
        bonus['jingdu'] = item('td').eq(4).text()
        bonus['chuquanchuxiri'] = item('td').eq(5).text()
        bonus['dengjiri'] = item('td').eq(6).text()
        shareBonus.append(bonus)

    maintable=d('table#sharebonus_2 tbody')
    rationBonus=[]
    for item in maintable('tr').items():
        bonus={}
        bonus['gonggaori'] = item('td').eq(0).text()
        # print(item('td').eq(1).text(),'   hhhhhh')
        bonus['peigufangan'] = Float(item('td').eq(1).text())
        bonus['peigujiage'] = Float(item('td').eq(2).text())
        bonus['jizhunguben'] = Float(item('td').eq(3).text())
        bonus['chuquanri'] = item('td').eq(4).text()
        bonus['dengjiri'] = item('td').eq(5).text()
        bonus['shangshiri'] = item('td').eq(-3).text()

        nexturl = item('td').eq(-1)
        try:
            nexturl = 'http://vip.stock.finance.sina.com.cn'+nexturl('a').attr('href')
        except Exception:
            nexturl = 'http://vip.stock.finance.sina.com.cn'
            pass

        nextext = yield from s.get(nexturl)
        nextext = yield from nextext.text(encoding='gb2312')
        d = pq(nextext)
        maintable = d('table#sharebonusdetail')
        bili = maintable('tr').eq(-4)
        bili = bili('td').eq(1).text()
        # bili = bili.replace('-','0')
        shiji = maintable('tr').eq(-6)
        shiji = shiji('td').eq(1).text()
        # shiji = shiji.replace(',','')
        # shiji = shiji.replace('-','0')
        bonus['shijipeigushu'] = Float(shiji)
        bonus['shijipeigubili'] = Float(bili)
        rationBonus.append(bonus)
        
    # print(maintable.html())
    return {'shareBonus': shareBonus, 'rationBonus': rationBonus, 'shareCode': sharecode}

      
    