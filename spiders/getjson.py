#!/usr/bin/env python
# coding=utf-8
'''
@Author: Jin X
@Date: 2020-02-25 22:18:16
@LastEditTime: 2020-02-26 00:44:20
'''
import requests
import time


stocks = ['AMZN', 'NVDA']
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
