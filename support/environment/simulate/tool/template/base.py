# coding=UTF-8


class BaseTemplate(object):

    def generate(self):
        raise NotImplementedError('Please imporlement this interface in subclass')

