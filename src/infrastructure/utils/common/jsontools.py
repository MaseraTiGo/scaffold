# coding=UTF-8

'''
Created on 2016年8月20日

@author: Administrator
'''

# import python standard package
import json
import datetime

# import thread package

# import my project package

def CJsonEncoder(json_list):
    for dic in json_list:
        for key, value in dic.items():
            if isinstance(value, datetime.datetime):
                dic[key] = value.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(value, datetime.date):
                dic[key] = value.strftime('%Y-%m-%d')
        if "children" in dic and len(dic["children"]) > 0:
            CJsonEncoder(dic["children"])
    return json_list

