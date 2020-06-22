# coding=UTF-8

'''
Created on 2018年7月16日

@author: Administrator
'''

# import python standard package
import re
# import thread package

# import my project package

class Security(object):

    @classmethod
    def mobile_encryption(cls, value):
        if value:
            p = re.compile(r'(\d{3})(\d{4})(\d{4})')
            value = p.sub(r'\1****\3', value)
        return value

    @classmethod
    def name_encryption(cls, value):
        if value:
            value = value.replace(value[1:], "*"*(len(value) - 1))
        return value

    @classmethod
    def other_encryption(cls, value):
        if value:
            value = value.replace(value[1:-1], "*"*(len(value) - 2))
        return value
