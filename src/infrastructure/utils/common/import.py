# coding=UTF-8

'''
Created on 2016-6-27

@author: YRK
'''

class LazyImport(object):

    def __init__(self, module_name):
        self.module_name = module_name
        self.module = None

    def __getattr__(self, name):
        if self.module is None:
            self.module = __import__(self.module_name)
        return getattr(self.module, name)
