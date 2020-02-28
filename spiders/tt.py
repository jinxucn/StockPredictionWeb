#!/usr/bin/env python
# coding=utf-8
'''
@Author: Jin X
@Date: 2020-02-28 11:20:37
@LastEditTime: 2020-02-28 11:53:21
'''
from dateutil import tz
from datetime import datetime, timezone, timedelta

tz_ny = tz.gettz('America/New_York')
now_ny = datetime.now(tz=tz_ny)
print(now_ny.strftime('%Y-%m-%d %H:%M:%S'))
print(now_ny.hour)
