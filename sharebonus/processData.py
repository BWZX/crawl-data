import asyncio
from pyquery import PyQuery as pq
import config


async def processData(s, data):
    '''
    data is from the http response in main module.
    '''
    d = pq(data)
    maintable=d('table#sharebonus_1 tbody')
    sharecode=d('div.tbtb01 h2').text()[1:]

    shareBonus=[]
    for item in maintable('tr').items():
        bonus={}
        bonus['gonggaori'] = item('td').eq(0).text()
        bonus['songgu'] = float(item('td').eq(1).text())
        bonus['zhuanzeng'] = float(item('td').eq(2).text())
        bonus['paixi'] = float(item('td').eq(3).text())
        bonus['jingdu'] = item('td').eq(4).text()
        bonus['chuquanchuxiri'] = item('td').eq(5).text()
        bonus['dengjiri'] = item('td').eq(6).text()
        shareBonus.append(bonus)

    maintable=d('table#sharebonus_2 tbody')
    rationBonus=[]
    for item in maintable('tr').items():
        bonus={}
        bonus['gonggaori'] = item('td').eq(0).text()
        bonus['peigufangan'] = float(item('td').eq(1).text())
        bonus['peigujiage'] = float(item('td').eq(2).text())
        bonus['jizhunguben'] = float(item('td').eq(3).text())
        bonus['chuquanri'] = item('td').eq(4).text()
        bonus['dengjiri'] = item('td').eq(5).text()
        bonus['shangshiri'] = item('td').eq(-3).text()

        nexturl = item('td').eq(-1)
        nexturl = 'http://vip.stock.finance.sina.com.cn'+nexturl('a').attr('href')
        nextext = await s.get(nexturl)
        nextext = await nextext.text(encoding='gb2312')
        d = pq(nextext)
        maintable = d('table#sharebonusdetail')
        bili = maintable('tr').eq(-4)
        bili = bili('td').eq(1).text()
        bili = bili.replace('-','0')
        shiji = maintable('tr').eq(-6)
        shiji = shiji('td').eq(1).text()
        shiji = shiji.replace(',','')
        shiji = shiji.replace('-','0')
        bonus['shijipeigushu'] = float(shiji)
        bonus['shijipeigubili'] = float(bili)
        rationBonus.append(bonus)
        
    # print(maintable.html())
    return {'shareBonus': shareBonus, 'rationBonus': rationBonus, 'shareCode': sharecode}

      
    