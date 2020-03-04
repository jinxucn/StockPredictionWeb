#!/usr/bin/env python
# coding=utf-8
'''
@Author: Jin X
@Date: 2020-03-01 15:09:55
@LastEditTime: 2020-03-03 22:59:59
'''
import pymysql
from threading import Lock


# database connector,
# the conn object is not thread safe
# use lock for thread synchronization
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

    # insert into real time table
    def insertRT(self, stockID, qTime, qOpen, qClose, qVolume, qLow, qHigh):
        self.lock.acquire()
        # in case connection is lose, reconnect it
        if not self.conn.open:
            self.reConn()
        try:
            with self.conn.cursor() as cursor:
                sql = 'INSERT INTO real_time VALUES (%s,%s,%s,%s,%s,%s,%s)'
                cursor.execute(sql, [stockID, qTime, qOpen,
                                     qClose, qVolume, qHigh, qLow])
            self.conn.commit()
        except Exception as e:
            print(e)
        self.lock.release()

    def closeConn(self):
        if self.conn.open:
            self.conn.close()

    def reConn(self):
        self.conn = pymysql.connect(
            host='jindb.c8ojtshzefs1.us-east-2.rds.amazonaws.com',
            user='stockpredictor',
            password='buyer',
            database='stocks',
            charset='utf8'
        )


# load history data to database
# @param type, str, 1h or 1d
# @param data, list(tuple): [(id,timestamp,quote...),...]
def loadHistory(type, data):
    conn = pymysql.connect(
        host='jindb.c8ojtshzefs1.us-east-2.rds.amazonaws.com',
        user='stockpredictor',
        password='buyer',
        database='stocks',
        charset='utf8'
    )
    try:
        with conn.cursor() as cursor:
            if type == '1h':
                sql = 'insert into history_hour values (%s,%s,%s,%s,%s,%s,%s)'
                cursor.executemany(sql, data)
            if type == '1d':
                sql = 'insert into history_day values (%s,%s,%s,%s,%s,%s,%s)'
                cursor.executemany(sql, data)
        conn.commit()
    finally:
        conn.close()
