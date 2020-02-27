#!/usr/bin/env python
# coding=utf-8
'''
@Author: Jin X
@Date: 2020-02-26 15:16:09
@LastEditTime: 2020-02-26 20:39:06
'''
from crawlHistory import *
import time
import threading


def periodSeq(t=1582641000):
    weekday = time.localtime().tm_wday
    cur = int(time.time())
    while cur-t > 86400:
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


if __name__ == '__main__':
