#!/usr/bin/env python
# coding=utf-8
'''
@Author: Jin X
@Date: 2020-02-25 22:18:16
@LastEditTime: 2020-02-26 15:21:45
'''
import requests
import time
import threading


stocksName = ['AMZN', 'NVDA']
url = 'https://query1.finance.yahoo.com/v8/finance/chart/AMZN'
payload = {
    'period1': 1519448400,
    'period2': int(time.time()),
    'interval': '1d',
    'includePrePost': 'true',
    # 'event': 'div%7Csplit%7Cearn',
    'lang': 'en-US',
    'region': 'US',
    # 'crumb': 'd1Iz5Itdme5',
    'corsDomain': 'finance.yahoo.com'
}


def periodSeq(t=1582641000):
    cur = int(time.time())
    while cur-t > 86400:
        yield (t-1, t+1)
        t += 86400


def requestStocks(periods):
    a = []
    for stock in stocksName:
        payload['symbol'] = stock
        payload['period1'] = periods[0]
        payload['period2'] = periods[1]
        r = requests.get(url, payload)
        result = r.json()['chart']['result'][0]
        # if result[]
        timestamp = result.get('timestamp')
        if timestamp is None:
            return a
        quote = result['indicators']['quote'][0]
        # zipped = zip(timestamp, quote['open'], quote['close'],
        #  quote['volume'], quote['low'], quote['high'])

        # for qTime, qOpen, qClose, qVolume, qLow, qHigh in zipped:
        #     print(str([qTime, qOpen, qClose, qVolume, qLow, qHigh])[1:-1])
        a.append((stock, timestamp, quote))
    return a


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
    for stock in stocks:
        payload['symbol'] = stock
        r = requests.get(url, payload)
        result = r.json()['chart']['result'][0]
        timestamp = result['timestamp']
        quote = result['indicators']['quote'][0]

        with open(r'./data/{}.csv'.format(stock), 'w+') as f:
            f.write('timestamp,open,close,volume,low,high\n')
            for qTime, qOpen, qClose, qVolume, qLow, qHigh in \
                    zip(timestamp, quote['open'], quote['close'],
                        quote['volume'], quote['low'], quote['high']):
                f.write(
                    str([qTime, qOpen, qClose, qVolume, qLow, qHigh])[1:-1]+'\n')

    # periods = periodSeq(1580308200)
    # requestThread(periods)
