#!/usr/bin/env python
# coding=utf-8
'''
@Author: Jin X
@Date: 2020-02-26 15:16:09
@LastEditTime: 2020-03-03 00:10:03
'''
from crawlHistory import *
from sqlConc import *
import time
# from multiprocessing import Process
from threading import Thread

db = DbConnector()


def requestThread(name, lastStamp):
    while True:
        weekday = time.localtime().tm_wday
        hour = time.localtime().tm_hour
        interval = '1m'
        print('{} :'.format(name), end='')
        if 0 <= weekday <= 4:
            if 9 <= hour < 16:
                print('state: sleep 1 minute')
                time.sleep(60)
            else:
                print('state: sleep 1 hour')
                time.sleep(3600)
                interval = '1h'
        else:
            print('state: sleep 1 day')
            time.sleep(3600*12)
        print('{} :lastStamp: {},state: crawling'.format(
            name, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(lastStamp))))
        curr = int(time.time())
        periods = [lastStamp, curr-curr % 60]
        timestamp, quote = requestStock(name, periods, interval)
        if timestamp is not None:
            # with open('./data/1m/{}.csv'.format(name), 'a+') as f:
            #     for qTime, qOpen, qClose, qVolume, qLow, qHigh in \
            #             zip(timestamp, quote['open'], quote['close'],
            #                 quote['volume'], quote['low'], quote['high']):
            #         if qOpen is not None:
            #             f.write(
            #                 str([qTime, qOpen, qClose, qVolume, qLow, qHigh])[1:-1]+'\n')
            #             lastStamp = qTime
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
        lastStamp[stock] = 1583182800  # Mar. 2 2020, 16:00 GMT-5
        with open('./data/1m/{}.csv'.format(stock), 'w+') as f:
            f.write('timestamp,open,close,volume,low,high\n')

    for stock in stockSymbols:
        # p = Process(target=requestThread, args=(stock, lastStamp[stock]))
        # p.start()
        t = Thread(target=requestThread, args=(stock, lastStamp[stock]))
        t.start()
