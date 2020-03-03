#!/usr/bin/env python
# coding=utf-8
'''
@Author: Jin X
@Date: 2020-02-26 15:16:09
@LastEditTime: 2020-03-03 15:57:34
'''
from crawlHistory import *
from sqlConc import *
import time
from threading import Thread

db = DbConnector()


# thread that crawl real time data
# depending on current time, sleep for a time period
# @param name: str,symbol of the stock
# @param lastStamp: int,in every loop, crawl data from last time stamp to current time stamp
def requestThread(name, lastStamp):
    while True:
        weekday = time.localtime().tm_wday
        hour = time.localtime().tm_hour
        interval = '1m'                         # default interval is 1m unless
        print('{} :'.format(name), end='')      # market is not open
        if 0 <= weekday <= 4:
            if 9 <= hour < 16:
                print('state: sleep 1 minute')
                time.sleep(60)
            else:
                db.closeConn()
                print('state: sleep 1 hour')
                time.sleep(3600)
                interval = '1h'
        else:
            db.closeConn()
            print('state: sleep 1 day')
            time.sleep(3600*12)
        print('{} :lastStamp: {},state: crawling'.format(
            name, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(lastStamp))))
        # calculate last exact minute
        curr = int(time.time())
        periods = [lastStamp, curr-curr % 60]
        timestamp, quote = requestStock(name, periods, interval)
        if timestamp is not None:
            # DISCARDED ! write the data into local files
            # with open('./data/1m/{}.csv'.format(name), 'a+') as f:
            #     for qTime, qOpen, qClose, qVolume, qLow, qHigh in \
            #             zip(timestamp, quote['open'], quote['close'],
            #                 quote['volume'], quote['low'], quote['high']):
            #         if qOpen is not None:
            #             f.write(
            #                 str([qTime, qOpen, qClose, qVolume, qLow, qHigh])[1:-1]+'\n')
            #             lastStamp = qTime

            # upload data to database
            for qTime, qOpen, qClose, qVolume, qLow, qHigh in \
                    zip(timestamp, quote['open'], quote['close'],
                        quote['volume'], quote['low'], quote['high']):
                if qOpen is not None and qVolume != 0:
                    db.insertRT(stockIDs[name], qTime, qOpen,
                                qClose, qVolume, qLow, qHigh)
                    lastStamp = qTime


if __name__ == '__main__':
    lastStamp = {}
    for stock in stockSymbols:
        # initialize the timestamp for every stock
        lastStamp[stock] = 1583245800  # Mar. 2 2020, 16:00 GMT-5
        # DISCARDED ! write to local files
        # with open('./data/1m/{}.csv'.format(stock), 'w+') as f:
        #     f.write('timestamp,open,close,volume,low,high\n')

    for stock in stockSymbols:
        # p = Process(target=requestThread, args=(stock, lastStamp[stock]))
        # p.start()
        t = Thread(target=requestThread, args=(stock, lastStamp[stock]))
        t.start()
