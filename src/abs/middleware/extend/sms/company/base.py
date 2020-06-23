# coding=UTF-8


class SmsBase(object):

    @property
    def label(self):
        return self.get_label()

    @property
    def name(self):
        return self.get_name()

    def get_name(cls):
        raise NotImplementedError("server need to implement get_name function")

    def get_label(cls):
        raise NotImplementedError("server need to implement get_label function")

    def get_sign_name(cls):
        raise NotImplementedError("server need to implement get_sign_name function")

    def send(self, *args, **kwargs):
        raise NotImplementedError("server need to implement send function")

