# coding=UTF-8

'''
Created on 2016年8月30日

@author: Administrator
'''

# import python standard package

# import thread package
from django.db.models.query import QuerySet
from infrastructure.core.exception.business_error import BusinessError
# import my project package

class Splitor(object):

    def __init__(self, cur_page, obj_list, size=10):
        self.size = size
        self.cur_page = cur_page
        self.data = None

        if self.cur_page > 0:
            self(obj_list)
        else:
            raise BusinessError("文件页数要求大于0")

    def json(self):
        return {
            'total' : self.total,
            'total_page':self.total_page,
            'size' : self.size,
            'cur_page' : self.cur_page,
        }

    def get_list(self):
        return self.data

    def __call__(self, obj_list):
        if isinstance(obj_list, QuerySet):
            self.total = obj_list.count()
        else:
            self.total = len(obj_list)

        self.total_page = int(self.total / self.size) + 1 \
                if self.total % self.size > 0 else int(self.total / self.size)
        self.data = list(obj_list[(self.cur_page - 1) * self.size : self.cur_page * self.size])
        return self

