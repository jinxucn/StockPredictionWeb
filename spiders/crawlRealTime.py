#!/usr/bin/env python
# coding=utf-8
'''
@Author: Jin X
@Date: 2020-02-26 15:16:09
@LastEditTime: 2020-02-28 12:17:04
'''
from crawlHistory import *
import time
from multiprocessing import Process


# 1582827540


def periodSeq(t=1582641000):
    cur = int(time.time())
    if cur - t > 60:
        return (t, cur)

    while cur-t > 60:
        yield (t-1, t+1)
        t += 86400


def requestThread(periodseq):
    try:
        period = next(periodseq)
    except StopIteration:
        return
    stocks = requestStocks(period)
    print('requested---'+time.strftime('%Y-%m-%d %H:%M:%S'))
    for stock in stocks:
        print('name {}, time {}'.format(stock[0], stock[1]))
    threading.Timer(5, requestThread, [periodseq]).start()


def requestProcess(name, lastStamp):
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
            with open('./data/1m/{}.csv'.format(name), 'a+') as f:
                for qTime, qOpen, qClose, qVolume, qLow, qHigh in \
                        zip(timestamp, quote['open'], quote['close'],
                            quote['volume'], quote['low'], quote['high']):
                    if qOpen is not None:
                        f.write(
                            str([qTime, qOpen, qClose, qVolume, qLow, qHigh])[1:-1]+'\n')
                        lastStamp = qTime


if __name__ == '__main__':
    lastStamp = {}
    for stock in stocksName:
        lastStamp[stock] = 1582741200  # Feb 26 2020, 13:20 GMT-5
        with open('./data/1m/{}.csv'.format(stock), 'w+') as f:
            f.write('timestamp,open,close,volume,low,high\n')

    for stock in stocksName:
        p = Process(target=requestProcess, args=(stock, lastStamp[stock]))
        p.start()
