from flask import Flask, render_template, url_for, request, jsonify, json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.ext.automap import automap_base
from flask_marshmallow import Marshmallow
from flask import render_template
from sqlalchemy.orm import sessionmaker
import time
import sqlite3


# Init app
app = Flask(__name__)

# configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://stockpredictor:buyer@jindb.c8ojtshzefs1.us-east-2.rds.amazonaws.com:3306/stocks'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
engine = create_engine(
    'mysql+pymysql://stockpredictor:buyer@jindb.c8ojtshzefs1.us-east-2.rds.amazonaws.com:3306/stocks')
cursor = engine.connect()
Session = sessionmaker(bind=engine)
session = Session()


db = SQLAlchemy(app)
ma = Marshmallow(app)



class Stock(db.Model):
    __tablename__ = 'stock_name'
    stock_id = db.Column(db.Integer, primary_key=True)
    stock_name = db.Column(db.String)
    #history_day = db.relationship('History_day', backref="comp_his_day", lazy=True )

    def __init__(self, stock_id, stock_name):
        self.stock_id = stock_id
        self.stock_name = stock_name


class History_day(db.Model):
    __tablename__ = 'history_day'
    stock_id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.Integer, primary_key=True)
    open = db.Column(db.Float)
    close = db.Column(db.Float)
    volume = db.Column(db.Float)
    low = db.Column(db.Float)
    high = db.Column(db.Float)

    def __init__(self, stock_id, day, open, close, volume, low, high):
        self.stock_id = stock_id
        self.day = day
        self.open = open
        self.close = close
        self.volume = volume
        self.low = low
        self.high = high


class Real_time(db.Model):
    __tablename__ = "real_time"
    stock_id = db.Column(db.Integer, primary_key=True)
    minute = db.Column(db.Integer, primary_key=True)
    open = db.Column(db.Float)
    close = db.Column(db.Float)
    volume = db.Column(db.Float)
    low = db.Column(db.Float)
    high = db.Column(db.Float)

    def __init__(self, stock_id, minute, open, close, volume, low, high):
        self.stock_id = stock_id
        self.minute = minute
        self.open = open
        self.close = close
        self.volume = volume
        self.low = low
        self.high = high

# product schema


class StockSchema(ma.Schema):
    class Meta:
        #model = Stock
        fields = ('stock_id', 'stock_name')


class History_daySchema(ma.Schema):
    class Meta:
        fields = ('day', 'open', 'close', 'volume', 'low', 'high')


class Real_timeSchema(ma.Schema):
    class Meta:
        fields = ('minute', 'open', 'close', 'volume', 'low', 'high')


# init Schema
stock_schema = StockSchema()
stocks_schema = StockSchema(many=True)
history_daySchema = History_daySchema()
history_daysSchema = History_daySchema(many=True)
real_timeSchema = Real_timeSchema()
real_timesSchema = Real_timeSchema(many=True)


# sample api get
@app.route('/', methods=['GET'])
def get():
    # return jsonify({"hello": "world"})
    return render_template('index.html')

# run server, get all stock ticker
@app.route('/stockNames', methods=['GET'])
def getTicker():
    all_products = Stock.query.all()
    result = stocks_schema.dump(all_products)
    # return jsonify([u.as_dict() for u in Stock.query.all()])
    return jsonify(result)


@app.route('/long', methods=['GET'])
def getLong():
    name = request.args.get("name")
    indicator = db.session.execute(
        'select * from indicator where stockID="{}"'.format(name))
    res = {
        'BBupper': [],
        'BBmiddle': [],
        'BBlower': [],
        'MACD': [],
        'slowD': [],
        'slowK': [],
        'timestamp': []
    }
    for i in indicator:
        res['BBupper'].append(i.BBupper)
        res['BBlower'].append(i.BBlower)
        res['timestamp'].append(i.TargetTime)
        res['MACD'].append(i.MACD_hist)
        res['slowD'].append(i.slowD)
        res['slowK'].append(i.slowK)
        res['BBmiddle'].append(i.BBmiddle)

    predict = db.session.execute(
        'select TargetTime,value from predict_long where stockID="{}"'.format(name))
    for p in predict:
        val = p[1]
        timestamp = p[0]
    res['predict'] = {
        'value': val,
        'timestamp': timestamp
    }
    return jsonify(res)


@app.route('/short', methods=['GET'])
def getShort():
    name = request.args.get("name")
    predict = db.session.execute(
        'select value,TargetTime from predict_short where stockID="{}"'.format(name))
    val = []
    timestamp = []
    for p in predict:
        val.append(p[0]),
        timestamp.append(p[1])
    res = {
        'Bayesian': {'value': val[0], 'timestamp': timestamp[0]},
        'SVM': {'value': val[1], 'timestamp': timestamp[1]},
    }
    return jsonify(res)


def timecontrol():
    lt = time.localtime()
    weekday = lt.tm_wday
    hour = lt.tm_hour
    minute = lt.tm_min
    if 0 <= weekday <= 4:
        if hour > 10 or (hour == 9 and minute >= 30):
            return time.mktime(
                (lt.tm_year, lt.tm_mon, lt.tm_mday, 9, 30, 0, 0, 0, 1))-1
        else:
            if weekday == 0:
                return time.mktime((lt.tm_year, lt.tm_mon, lt.tm_mday-3, 9, 30, 0, 0, 0, 1))-1
            else:
                return time.mktime((lt.tm_year, lt.tm_mon, lt.tm_mday-1, 9, 30, 0, 0, 0, 1))-1
    elif weekday == 5:
        return time.mktime((lt.tm_year, lt.tm_mon, lt.tm_mday-1, 9, 30, 0, 0, 0, 1))-1
    elif weekday == 6:
        return time.mktime((lt.tm_year, lt.tm_mon, lt.tm_mday-2, 9, 30, 0, 0, 0, 1))-1

# sql #2:Get the highest stock price of any company in the last ten days
def getHigh(stockID):
    sql = '''select max(h.high)
                from history_day as h 
                where h.day >= unix_timestamp(current_date() - interval 10 day) 
                and h.stock_ID={}'''.format(stockID)
    result = cursor.execute(sql)
    for i in result:
        res = i[0]
    return res
# sql #3: Average stock price of any company in the latest one year
# we use history_day.high for calculation
def getAvg(stockID):
    sql = '''select avg(h.close) 
                from history_day as h 
                where h.day >=  unix_timestamp(current_date()- interval 1 year) 
                and h.stock_ID={}'''.format(stockID)
    result = cursor.execute(sql)
    for i in result:
        res = i[0]
    return res

# sql #4: Lowest stock price for any company in the latest one year
# use history_day.low for calculation
def getLow(stockID):
    sql = '''select min(h.low)
                from history_day as h 
                where h.day >= unix_timestamp(current_date()- interval 1 year)
                and h.stock_ID={}'''.format(stockID)
    result = cursor.execute(sql)
    for i in result:
        res = i[0]
    return res

# sql #5 List the ids of companies along with their name who have the average stock price lesser than the lowest of any of the Selected Company in the latest one year.
def getLess(stockID):
    sql = '''select s1.stock_name from stock_name as
    s1 join history_day as h1 on (s1.stock_ID=h1.stock_ID) 
    where h1.day >= unix_timestamp(current_date() - interval 1 year) 
    group by s1.stock_name having avg(h1.close) > (select min(h2.low) 
    from stock_name as s2 join history_day as h2 on(s2.stock_ID=h2.stock_ID) 
    where h2.day >= unix_timestamp(current_date() - interval 1 year) and s2.stock_ID={})'''.format(stockID)
    result = db.session.execute(sql)
    name = []
    for i in result:
        name.append(i[0])
    return name
# get historical/real time data of each company
@app.route('/stockdata', methods=['GET'])
def getReal():
    name = request.args.get("name")
    datatype = request.args.get("type")
    res = {}
    if datatype == "history":
        stock_details = Stock.query.filter_by(stock_name=name).first()
        stock_detail = stock_details.stock_id
        detail = History_day.query.filter_by(stock_id=stock_detail)
        list_time = [u.day for u in detail]
        res['high10day'] = getHigh(stock_detail)
        res['avg1year'] = getAvg(stock_detail)
        res['low1year'] = getLow(stock_detail)
        res['less'] = getLess(stock_detail)

    elif datatype == "realtime":
        lastOpenTime = timecontrol()
        stock = Stock.query.filter_by(stock_name=name).first()
        real_id = stock.stock_id
        detail = Real_time.query.filter(
            Real_time.stock_id == real_id, Real_time.minute > lastOpenTime)
        list_time = [u.minute for u in detail]
        # detail = Real_time.query.filter(
        #     stock_detail.stock_id == real_id, Real_time.minute > 1588339920)

    list_open = [u.open for u in detail]
    # list_time = [u.minute for u in detail]
    list_close = [u.close for u in detail]
    list_volume = [u.volume for u in detail]
    list_high = [u.high for u in detail]
    list_low = [u.low for u in detail]
    res['name'] = name
    res['open'] = list_open
    res['timestamp'] = list_time
    res['close'] = list_close
    res['volume'] = list_volume
    res['high'] = list_high
    res['low'] = list_low
    return jsonify(res)


# sql question 1: list of all companies with their latest stock price (real time latest)
@app.route('/listsReal', methods=['GET'])
def getlist():
    sql = 'select max(minute) as minute,close,stock_ID from real_time group by stock_ID;'
    result = cursor.execute(sql)
    res = []
    for i in result:
        res.append({
            'id': i.stock_ID,
            'price': i.close,
            'timestamp': i.minute
        })
    return jsonify(res)




if __name__ == '__main__':
    # app.run(debug=True)

    sql = '''delete from history_day where day>=1588858200;'''
    db.session.execute(sql)
