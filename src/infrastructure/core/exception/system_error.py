# coding=UTF-8

'''
Created on 2016-7-4

@author: YRK
'''


from infrastructure.core.exception.base import BaseError


class SysCodes(object):
    DEFAULT = 10001


class SysError(BaseError):

    code = SysCodes.DEFAULT
    desc = "系统运行错误"

    def __init__(self, e, *args, **kwargs):
        super(SysError, self).__init__(*args, **kwargs)
        self.e = e

    def generate_msg(self, *args, **kwargs):
        return self.desc
