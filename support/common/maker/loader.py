# coding=UTF-8


class BaseLoader(object):

    def generate(self):
        raise NotImplementedError(
            'Please imporlement this interface in subclass'
        )
