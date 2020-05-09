#!/usr/bin/env python
# coding=utf-8
'''
@Author: Jin X
@Date: 2020-05-09 12:46:26
@LastEditTime: 2020-05-09 16:39:19
'''
import pandas as pd
from util import *
from sqlalchemy import create_engine
# stockID = 'AMD'
# path = '../../spiders/data/1d/' + stockID + '.csv'
# df2 = df = pd.read_csv(path)
# df2 = df2.iloc[:, [0, 2, 4, 5]]
# data_np = df2.to_numpy().transpose()
# data_np[data_np == " None"] = "0"
# print(data_np.astype(float))
path = '../result/lstm.csv'
df = pd.read_csv(path)
df = df.iloc[:, 1:]
print(df)

drive = 'mysql+pymysql://stockpredictor:buyer@jindb.c8ojtshzefs1.us-east-2.rds.amazonaws.com:3306/stocks'
engine = create_engine(drive)
pd.io.sql.to_sql(df, 'predict_long', con=engine,
                 index=False, if_exists='replace')

# data = import_file(4, '1d')
# print(data)

# drive = 'mysql+pymysql://stockpredictor:buyer@jindb.c8ojtshzefs1.us-east-2.rds.amazonaws.com:3306/stocks'
# engine = create_engine(drive)
# sql = ''' select day,close,low,high from history_day where stock_id=2 '''
# df = pd.read_sql_query(sql, engine)
# data_np2 = df.to_numpy().transpose()
# data_np2[data_np2 == " None"] = "0"
# # print(data_np2.astype(float))
