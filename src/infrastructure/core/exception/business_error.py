# coding=UTF-8

'''
Created on 2016-7-4

@author: YRK
'''


from infrastructure.core.exception.base import BaseError


class BusinessCodes(object):
    DEFAULT = 40001


class BusinessError(BaseError):

    code = BusinessCodes.DEFAULT
    desc = "业务逻辑错误"
