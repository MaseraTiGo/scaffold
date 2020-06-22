# coding=UTF-8

from model.models import Role

class LoaderHelper(object):

    @classmethod
    def loading(cls):
        return Role.query().order_by('create_time')
