#!/usr/bin/env python
# coding=utf-8
'''
@Author: Jin X
@Date: 2020-03-01 15:09:55
@LastEditTime: 2020-03-03 00:07:42
'''
import pymysql
from threading import Lock


class DbConnector:
    def __init__(self):
        self.conn = pymysql.connect(
            host='jindb.c8ojtshzefs1.us-east-2.rds.amazonaws.com',
            user='stockpredictor',
            password='buyer',
            database='stocks',
            charset='utf8'
        )
        self.lock = Lock()

    def insertRT(self, stockID, qTime, qOpen, qClose, qVolume, qLow, qHigh):
        self.lock.acquire()
        with self.conn.cursor() as cursor:

            sql = 'INSERT INTO real_time VALUES (%s,%s,%s,%s,%s,%s,%s)'
            cursor.execute(sql, [stockID, qTime, qOpen,
                                 qClose, qVolume, qHigh, qLow])
        self.conn.commit()
        self.lock.release()

    def closeConn(self):
        self.conn.close()

    def reConn(self):
        self.conn = pymysql.connect(
            host='jindb.c8ojtshzefs1.us-east-2.rds.amazonaws.com',
            user='stockpredictor',
            password='buyer',
            database='stocks',
            charset='utf8'
        )
