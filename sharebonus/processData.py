import asyncio
from pyquery import PyQuery as pq
import config


async def processData(data):
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
        bonus['songgu'] = item('td').eq(1).text()
        bonus['zhuanzeng'] = item('td').eq(2).text()
        bonus['paixi'] = item('td').eq(3).text()
        bonus['jingdu'] = item('td').eq(4).text()
        bonus['chuquanchuxiri'] = item('td').eq(5).text()
        bonus['dengjiri'] = item('td').eq(6).text()
        shareBonus.append(bonus)

    maintable=d('table#sharebonus_2 tbody')
    rationBonus=[]
    for item in maintable('tr').items():
        bonus={}
        bonus['gonggaori'] = item('td').eq(0).text()
        bonus['peigufangan'] = item('td').eq(1).text()
        bonus['peigujiage'] = item('td').eq(2).text()
        bonus['jizhunguben'] = item('td').eq(3).text()
        bonus['chuquanri'] = item('td').eq(4).text()
        bonus['dengjiri'] = item('td').eq(5).text()
        bonus['shangshiri'] = item('td').eq(-1).text()
        rationBonus.append(bonus)
        
    # print(maintable.html())
    return {'shareBonus': shareBonus, 'rationBonus': rationBonus, 'shareCode': sharecode}

      
    