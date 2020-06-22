# coding=UTF-8

'''
Created on 2016-7-4

@author: YRK
'''


from infrastructure.core.exception.base import BaseError, BaseErrorManager

class ApiCodes(object):
    INTERFACE_NOT_EXIST = 30001
    INTERFACE_FREQUENTLY = 30002
    INTERFACE_TIMEOUT = 30003
    INTERFACE_PARATERS_LOST = 30004
    INTERFACE_PARATERS_PARSE_WRONG = 30005
    INTERFACE_PARATERS_TYPE_ERROR = 30006
    INTERFACE_TOKEN_INVALIED = 30007
    INTERFACE_TOKEN_DUE = 30008
    INTERFACE_TOKEN_RENEW_ERROR = 30009

    CHOICES = (
        (INTERFACE_NOT_EXIST, '请求的接口不存在'),
        (INTERFACE_FREQUENTLY, '请求频率超过上限'),
        (INTERFACE_TIMEOUT, '请求接口超过时效性'),
        (INTERFACE_PARATERS_LOST, '缺失参数({}),请参考API文档'),
        (INTERFACE_PARATERS_PARSE_WRONG, '参数格式不对({}),请查阅API文档, 错误信息:{}'),
        (INTERFACE_TOKEN_INVALIED, 'auth_token不存在'),
        (INTERFACE_TOKEN_DUE, 'auth_token已过期,请重新获取'),
        (INTERFACE_TOKEN_RENEW_ERROR, 'auth_token续签失败,请重新获取'),
        (INTERFACE_PARATERS_TYPE_ERROR , "参数({})值非法，请参考API文档"),
    )


class ApiError(BaseError):

    @classmethod
    def get_flag(cls):
        return 'api'


def bind_error(**config):

    class TempApiError(ApiError):
        code = config.get('code', 0)
        desc = config.get('desc', "")
        template = config.get('desc', "")

    return TempApiError


class ApiErrorManager(BaseErrorManager):

    _valid_errors = [ key for key, _ in ApiCodes.CHOICES]

    def __init__(self):
        self._error = {}
        self._loads()

    def _loads(self):
        for code, desc in ApiCodes.CHOICES:
            api_error = bind_error(code=code, desc=desc)
            self.regiter(api_error)


api_errors = ApiErrorManager()


if __name__ == "__main__":
    for api_error in api_errors._error.values():
        print(api_error)
