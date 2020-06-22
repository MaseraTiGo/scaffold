# coding=UTF-8

'''
Created on 2016-6-30

@author: YRK
'''

class Single(object):

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(Single, cls).__new__(cls, *args, **kwargs)
        return cls._instance
