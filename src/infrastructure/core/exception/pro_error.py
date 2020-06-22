# coding=UTF-8

'''
Created on 2016-7-4

@author: YRK
'''


from infrastructure.core.exception.base import BaseError, BaseErrorManager


class ProtocolCodes(object):
    PROTOCOL_DATA_EXCHANGE = 20001
    PROTOCOL_LOST_PARAM = 20002
    PROTOCOL_FORMAT_ERROR = 20003
    PROTOCOL_TIMEROUT = 20004

    CHOICES = (
        (PROTOCOL_DATA_EXCHANGE, '数据被串改'),
        (PROTOCOL_LOST_PARAM, '协议参数丢失 ({})'),
        (PROTOCOL_FORMAT_ERROR, '协议参数 {} 应为 {} 类型'),
        (PROTOCOL_TIMEROUT, '数据访问超时'),
    )


class ProtocolError(BaseError):

    @classmethod
    def get_flag(cls):
        return 'pro'


def bind_error(**config):

    class TempProtocolError(ProtocolError):
        code = config.get('code', 0)
        desc = config.get('desc', "")
        template = config.get('desc', "")

    return TempProtocolError


class ProtocolErrorManager(BaseErrorManager):

    _valid_errors = [key for key, _ in ProtocolCodes.CHOICES]

    def __init__(self):
        self._error = {}
        self._loads()

    def _loads(self):
        for code, desc in ProtocolCodes.CHOICES:
            pro_error = bind_error(code=code, desc=desc)
            self.regiter(pro_error)


pro_errors = ProtocolErrorManager()
