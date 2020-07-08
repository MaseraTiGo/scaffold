# coding=UTF-8

'''
Created on 2020年7月8日

@author: Roy
'''

from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet
from infrastructure.core.exception.business_error import BusinessError
from infrastructure.core.field.base import CharField, DictField, IntField, ListField, DatetimeField, DateField, BooleanField

from agile.base.api import NoAuthorizedApi
from abs.service.customer.manager import CustomerAccountServer


class Renew(NoAuthorizedApi):

    request = with_metaclass(RequestFieldSet)
    request.auth_token = RequestField(CharField, desc = "用户凭证")
    request.renew_flag = RequestField(CharField, desc = "续签标识")

    response = with_metaclass(ResponseFieldSet)
    response.access_token = ResponseField(CharField, desc = "访问凭证")
    response.renew_flag = ResponseField(CharField, desc = "续签标识")
    response.expire_time = ResponseField(CharField, desc = "到期时间")

    @classmethod
    def get_desc(cls):
        return "客户重新续签标识"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        token = CustomerAccountServer.renew_token(request.auth_token, request.renew_flag)
        return token

    def fill(self, response, token):
        response.access_token = token.auth_token
        response.renew_flag = token.renew_flag
        response.expire_time = token.expire_time
        return response
