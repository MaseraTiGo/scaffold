# coding=UTF-8

'''
Created on 2016年8月6日

@author: Administrator
'''

import time
import datetime


def add_suffix(origin, flag = None):
    if flag is None:
        flag = str(time.time())
    return "{}{}".format(origin, str(flag))


def generate_identity():
    return str(time.time())[:18]


def serializable_date(year, month, date):
    return datetime.date(year, month, date).strftime("%Y-%m-%d")


def serializable_datetime(year, month, date, hour = 0, minutes = 0, seconds = 0):
    return datetime.datetime(year, month, date, hour, minutes, seconds)\
            .strftime("%Y-%m-%d %H:%M:%S")
