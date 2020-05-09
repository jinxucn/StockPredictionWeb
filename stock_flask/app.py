from flask import Flask, render_template, url_for, request, jsonify, json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.ext.automap import automap_base
from flask_marshmallow import Marshmallow
from flask import render_template
import time

# Init app
app = Flask(__name__)

# configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://stockpredictor:buyer@jindb.c8ojtshzefs1.us-east-2.rds.amazonaws.com:3306/stocks'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
# init ma
ma = Marshmallow(app)

#  def as_dict(self):
#   return {c.name: getattr(self, c.name) for c in self.__table__.columns}


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


# sql question 1 get real time data
@app.route('/stockdata', methods=['GET'])
def getReal():
    name = request.args.get("name")
    datatype = request.args.get("type")
    if datatype == "history":
        stock_details = Stock.query.filter_by(stock_name=name).first()
        stock_detail = stock_details.stock_id
        detail = History_day.query.filter_by(stock_id=stock_detail)
        list_time = [u.day for u in detail]

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
    return jsonify({"name": name, "open": list_open, "timestamp": list_time,
                    "close": list_close, "volume": list_volume,
                    "high": list_high, "low": list_low
                    })



if __name__ == '__main__':
    app.run(debug=True)
