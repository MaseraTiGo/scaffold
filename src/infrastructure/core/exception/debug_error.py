# coding=UTF-8

'''
Created on 2016-7-4

@author: YRK
'''

from infrastructure.core.exception.base import BaseError


class DebugCodes(object):
    DEBUG_CODE = 999999


class DebugError(BaseError):

    code = DebugCodes.DEBUG_CODE
    desc = "开发阶段框架检查出的错误"
