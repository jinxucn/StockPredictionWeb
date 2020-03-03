#!/usr/bin/env python
# coding=utf-8
'''
@Author: Jin X
@Date: 2020-02-25 22:18:16
@LastEditTime: 2020-03-02 23:37:48
'''
import requests

# stock symbols for Nvida, AMD, Alibaba, Coca-cola, Disney
# Amazon, BiliBili, Netease, Google, Intel
stockSymbols = ['NVDA', 'AMD', 'BABA', 'KO', 'DIS',
                'AMZN', 'BILI', 'NTES', 'GOOG', 'INTC']
stockIDs = {}
for i in range(len(stockSymbols)):
    stockIDs[stockSymbols[i]] = [i+1]

url = 'https://query1.finance.yahoo.com/v8/finance/chart/AMZN'


payload = {                                 # Default time period
    'period1': 1582295400-3600*24*365,      # From Feb. 21 2019
    'period2': 1583159400,                  # To   Mar. 2 2020
    'interval': '1d',
    'includePrePost': 'true',
    # 'event': 'div%7Csplit%7Cearn',
    'lang': 'en-US',
    'region': 'US',
    # 'crumb': 'd1Iz5Itdme5',
    'corsDomain': 'finance.yahoo.com'
}


def requestStocks(periods):
    a = []
    for stock in stockSymbols:
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
        a.append((stock, timestamp, quote))
    return a


def requestStock(name, periods, interval):
    payload['symbol'] = name
    payload['period1'] = periods[0]
    payload['period2'] = periods[1]
    payload['interval'] = interval
    r = requests.get(url, payload)
    result = r.json()['chart']['result'][0]
    timestamp = result.get('timestamp')
    if timestamp is None:
        return None, None
    quote = result['indicators']['quote'][0]
    return timestamp, quote


if __name__ == '__main__':
    for stock in stockSymbols:
        payload['symbol'] = stock
        payload['interval'] = '1d'
        r = requests.get(url, payload)
        result = r.json()['chart']['result'][0]
        timestamp = result['timestamp']
        quote = result['indicators']['quote'][0]

        with open(r'./data/1d/{}.csv'.format(stock), 'w+') as f:
            f.write('timestamp,open,close,volume,low,high\n')
            for qTime, qOpen, qClose, qVolume, qLow, qHigh in \
                    zip(timestamp, quote['open'], quote['close'],
                        quote['volume'], quote['low'], quote['high']):
                f.write(
                    str([qTime, qOpen, qClose, qVolume, qLow, qHigh])[1:-1]+'\n')

        payload['interval'] = '1h'
        r = requests.get(url, payload)
        result = r.json()['chart']['result'][0]
        timestamp = result['timestamp']
        quote = result['indicators']['quote'][0]

        with open(r'./data/1h/{}.csv'.format(stock), 'w+') as f:
            f.write('timestamp,open,close,volume,low,high\n')
            for qTime, qOpen, qClose, qVolume, qLow, qHigh in \
                    zip(timestamp, quote['open'], quote['close'],
                        quote['volume'], quote['low'], quote['high']):
                f.write(
                    str([qTime, qOpen, qClose, qVolume, qLow, qHigh])[1:-1]+'\n')
