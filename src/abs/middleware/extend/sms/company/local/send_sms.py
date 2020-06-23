# coding=UTF-8

from .base import SsoBase


class Sms(SsoBase):

    def __init__(self):
        super(Sms, self).__init__()
        self._flag = "api"

    def get_url(self):
        return 'https://sms.rong-mi.cn:443'

    def send_sms(self, **param):
        """发送"""
        param.update({"api":"sms.send", "signType":"rsa"})
        return self._request_api(**param)


local_sms_middleware = Sms()
