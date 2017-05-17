# Create your models here.

from pymongo import TEXT
from pymongo.operations import IndexModel
from pymodm import connect, fields, MongoModel, EmbeddedMongoModel


# from securities.models import Security


# Connect to MongoDB first. PyMODM supports all URI options supported by
# PyMongo. Make sure also to specify a database in the connection string:
connect('mongodb://node0:27017/quant')

class Exchange(MongoModel):
    name = fields.CharField()

    # class Meta:
    #     final = True

class Securities(MongoModel):
    name = fields.CharField()
    code = fields.CharField()
    exchange_id = fields.ReferenceField(Exchange)
    industry = fields.CharField()

    # class Meta:
    #     final = True

class PriceEvent(MongoModel):
    security_id = fields.ReferenceField(Securities)
    event_type = fields.IntegerField()
    change_at = fields.IntegerField()
    price_before = fields.FloatField()
    price_after = fields.FloatField()
    ratio = fields.FloatField()

    class Meta:
        final = True

class TimeSeries(MongoModel):
    security = fields.ReferenceField(Securities)
    metric = fields.CharField()
    tag = fields.CharField()
    start_at = fields.DateTimeField()
    end_at = fields.DateTimeField()

    class Meta:
        final = True

class ShareBonus(MongoModel):
    gupiao = fields.ReferenceField(Securities)
    gonggaori = fields.CharField(blank=True)
    chuquanchuxiri = fields.CharField(blank=True)
    dengjiri = fields.CharField(blank=True)
    songgu = fields.FloatField()
    zhuanzeng = fields.FloatField()
    paixi = fields.FloatField()
    jingdu = fields.CharField(blank=True)

    class Meta:
        final = True

class ShareRation(MongoModel):
    gupiao = fields.ReferenceField(Securities)
    gonggaori = fields.CharField(blank=True)
    shangshiri = fields.CharField(blank=True)
    chuquanri = fields.CharField(blank=True)
    dengjiri = fields.CharField(blank=True)
    peigufangan = fields.FloatField()
    peigujiage = fields.FloatField()    
    jizhunguben = fields.FloatField()
    
    shijipeigushu = fields.FloatField()
    shijipeigubili = fields.FloatField()

    class Meta:
        final = True

class Finance(MongoModel):
    security = fields.ReferenceField(Securities)
    time = fields.CharField(blank=True)       #'2017.1' 季度
    esp = fields.FloatField()       #每股收益
    eps_yoy = fields.FloatField()       #每股收益同比(%)
    bvps = fields.FloatField()       #每股净资产
    roe = fields.FloatField()       #净资产收益率(%)
    epcf = fields.FloatField()       #每股现金流量(元)
    net_profits = fields.FloatField()       #净利润(万元)
    profits_yoy = fields.FloatField()       #净利润同比(%)
    distrib = fields.CharField(blank=True)       #分配方案
    report_date = fields.CharField(blank=True)       #发布日期
    #roe = fields.FloatField()       #净资产收益率(%)
    net_profit_ratio = fields.FloatField()       #净利率(%)
    gross_profit_rate = fields.FloatField()       #毛利率(%)
    #net_profits = fields.FloatField()       #净利润(万元)
    #esp = fields.FloatField()       #每股收益
    business_income = fields.FloatField()       #营业收入(百万元)
    bips = fields.FloatField()       #每股主营业务收入(元)
    arturnover = fields.FloatField()       #应收账款周转率(次)
    arturndays = fields.FloatField()       #应收账款周转天数(天)
    inventory_turnover = fields.FloatField()       #存货周转率(次)
    inventory_days = fields.FloatField()       #存货周转天数(天)
    currentasset_turnover = fields.FloatField()       #流动资产周转率(次)
    currentasset_days = fields.FloatField()       #流动资产周转天数(天)
    mbrg = fields.FloatField()       #主营业务收入增长率(%)
    nprg = fields.FloatField()       #净利润增长率(%)
    nav = fields.FloatField()       #净资产增长率
    targ = fields.FloatField()       #总资产增长率
    epsg = fields.FloatField()       #每股收益增长率
    seg = fields.FloatField()       #股东权益增长率
    currentratio = fields.FloatField()       #流动比率
    quickratio = fields.FloatField()       #速动比率
    cashratio = fields.FloatField()       #现金比率
    icratio = fields.FloatField()       #利息支付倍数
    sheqratio = fields.FloatField()       #股东权益比率
    adratio = fields.FloatField()       #股东权益增长率
    cf_sales = fields.FloatField()       #经营现金净流量对销售收入比率
    rateofreturn = fields.FloatField()       #资产的经营现金流量回报率
    cf_nm = fields.FloatField()       #经营现金净流量与净利润的比率
    cf_liabilities = fields.FloatField()       #经营现金净流量对负债比率
    cashflowratio = fields.FloatField()       #现金流量比率

    date = fields.CharField(blank=True)        #报告日期
    nums = fields.FloatField()        #基金家数
    nlast = fields.FloatField()        #与上期相比（增加或减少了）
    count = fields.FloatField()        #基金持股数（万股）
    clast = fields.FloatField()        #与上期相比
    amount = fields.FloatField()        #基金持股市值
    ratio = fields.FloatField()        #占流通盘比率

    type = fields.CharField(blank=True)       #业绩变动类型【预增、预亏等】
    report_date = fields.CharField(blank=True)       #发布日期
    pre_eps = fields.FloatField()       #上年同期每股收益
    range = fields.FloatField()       #业绩变动范围

    class Meta:
        final = True

arglist=(    
    'time',
    'esp',
    'eps_yoy',
    'bvps',
    'roe',
    'epcf',
    'net_profits',
    'profits_yoy',
    'distrib',
    'report_date',
    'net_profit_ratio',
    'gross_profit_rate',
    'business_income',
    'bips',
    'arturnover',
    'arturndays',
    'inventory_turnover',
    'inventory_days',
    'currentasset_turnover',
    'currentasset_days',
    'mbrg',
    'nprg',
    'nav',
    'targ',
    'epsg',
    'seg',
    'currentratio',
    'quickratio',
    'cashratio',
    'icratio',
    'sheqratio',
    'adratio',
    'cf_sales',
    'rateofreturn',
    'cf_nm',
    'cf_liabilities',
    'cashflowratio',

    'date',
    'nums',
    'nlast',
    'count',
    'clast',
    'amount',
    'ratio',

    'type',
    'report_date',
    'pre_eps',
    'range'
)

    

if __name__ == '__main__':
    


    Exchange(name='j股市').save()
    # exchange=Exchange.objects.raw({'name':'沪深股市'}).all()[0]._id
    # print(exchange)
    # Securities('test','test',exchange).save()
    # for post in Securities.objects.raw({'code': '000001'}):
    #     print(post.name + ' by ' + post.code)

    for obj in Exchange.objects.all():
        print(obj.name)
    # for obj in Securities.objects.all():
    #     print(obj.name)
