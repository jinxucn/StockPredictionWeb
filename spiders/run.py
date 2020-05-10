#!/usr/bin/env python
# coding=utf-8
'''
@Author: Jin X
@Date: 2020-05-06 21:08:47

'''
import requests
import time
from sqlConc import getLatestTime, load

stockSymbols = ['NVDA', 'AMD', 'BABA', 'KO', 'DIS',
                'AMZN', 'BILI', 'NTES', 'GOOG', 'INTC']


stockIDs = {}
for i in range(len(stockSymbols)):
    stockIDs[stockSymbols[i]] = i+1


def timecontrol():
    lt = time.localtime()
    weekday = lt.tm_wday
    hour = lt.tm_hour
    minute = lt.tm_min
    if 0 <= weekday <= 4:
        if (10 <= hour < 16) or (hour == 9 and minute >= 30):
            return True, 60
        elif hour >= 16:
            if 0 <= weekday < 4:
                nextOpenTime = time.mktime(
                    (lt.tm_year, lt.tm_mon, lt.tm_mday+1, 9, 30, 0, 0, 0, 1))
                return False, nextOpenTime-time.mktime(lt), True
            else:
                nextOpenTime = time.mktime(
                    (lt.tm_year, lt.tm_mon, lt.tm_mday+3, 9, 30, 0, 0, 0, 1))
                return False, nextOpenTime-time.mktime(lt), True
        elif hour < 9 or (hour == 9 and minute < 30):
            nextOpenTime = time.mktime(
                (lt.tm_year, lt.tm_mon, lt.tm_mday, 9, 30, 0, 0, 0, 1))
            return False, nextOpenTime-time.mktime(lt)
    else:
        if weekday == 5:
            nextOpenTime = time.mktime(
                (lt.tm_year, lt.tm_mon, lt.tm_mday+2, 9, 30, 0, 0, 0, 1))
        elif weekday == 6:
            nextOpenTime = time.mktime(
                (lt.tm_year, lt.tm_mon, lt.tm_mday+1, 9, 30, 0, 0, 0, 1))
        return False, nextOpenTime-time.mktime(lt)


def request(type):
    res = []
    curr = int(time.time())
    latest = getLatestTime(type, [i for i in range(1, len(stockSymbols)+1)])
    payload = {
        'period1': 1,
        'period2':  curr - curr % 60,
        'interval': type,
        'includePrePost': 'true',
        'lang': 'en-US',
        'region': 'US',
        'corsDomain': 'finance.yahoo.com'
    }
    for stock in stockSymbols:
        url = 'https://query1.finance.yahoo.com/v8/finance/chart/'+stock
        payload['period1'] = latest[stockIDs[stock]]
        payload['symbol'] = stock
        r = requests.get(url, payload)
        result = r.json()['chart']['result'][0]
        timestamp = result.get('timestamp', None)
        if timestamp:
            quote = result['indicators']['quote'][0]

            sid = [stockIDs[stock] for i in range(len(timestamp))]
            data = list(
                zip(sid, timestamp, quote['open'], quote['close'], quote['volume'],
                    quote['low'], quote['high']))
            for d in data:
                if d[4] is not None:
                    res.append(d)
    return res


def main():
    while True:
        cc = timecontrol()
        sleep = cc[1]
        if len(cc) == 3:
            oneday = request('1d')
            load('1d', oneday)
            onehour = request('1h')
            load('1h', onehour)
        else:
            isopen = cc[0]
            if isopen:
                oneminute = request('1m')
                load('1m', oneminute)
        print(sleep)
        time.sleep(sleep)


if __name__ == "__main__":
    # lt = time.localtime()
    # nextOpenTime = time.mktime(
    #     (lt.tm_year, lt.tm_mon, lt.tm_mday+3, 9, 30, 0, 0, 0, 1))
    # a = foo()

    main()
