# coding=UTF-8

from model.models import Department

class LoaderHelper(object):

    @classmethod
    def loading(cls):
        return Department.query().order_by('create_time')
