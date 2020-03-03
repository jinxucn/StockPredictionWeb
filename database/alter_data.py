# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 12:55:32 2020

@author: acer
"""

import pandas as pd

stocks = ['NVDA', 'AMD', 'BABA', 'KO', 'DIS',
         'AMZN', 'BILI', 'NTES', 'GOOG', 'INTC']
ind = 1
for stock in stocks:
    data_d = pd.read_csv(r'C:\Users\acer\Documents\GitHub\StockPredictionWeb\spiders\data\1d\{}.csv'.format(stock), header = 0)
    data_d.insert(0,'stock_id',[ind]*len(data_d.iloc[:,1])) 
    data_d.to_csv(r'C:\Users\acer\Desktop\rutgers_semester2\332586\project\1d\{}.csv'.format(stock), header = None, index = None)
    
    data_h = pd.read_csv(r'C:\Users\acer\Documents\GitHub\StockPredictionWeb\spiders\data\1h\{}.csv'.format(stock), header = 0)
    data_h.insert(0,'stock_id',[ind]*len(data_h.iloc[:,1])) 
    data_h.to_csv(r'C:\Users\acer\Desktop\rutgers_semester2\332586\project\1h\{}.csv'.format(stock), header = None, index = None)
    
    ind = ind + 1


