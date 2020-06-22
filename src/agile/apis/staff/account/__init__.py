# coding=UTF-8

'''
Created on 2016年7月23日

@author: Roy
'''

from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet
from infrastructure.core.exception.business_error import BusinessError
from infrastructure.core.field.base import CharField, DictField, IntField, ListField, DatetimeField, DateField, BooleanField

from agile.apis.base import StaffAuthorizedApi
from agile.apis.base import NoAuthrizedApi
from abs.service.staff.manager import StaffServer, StaffAccountServer


class Login(NoAuthrizedApi):
    """员工登录接口"""
    request = with_metaclass(RequestFieldSet)
    request.username = RequestField(CharField, desc = "账号")
    request.password = RequestField(CharField, desc = "密码")

    response = with_metaclass(ResponseFieldSet)
    response.access_token = ResponseField(CharField, desc = "访问凭证")
    response.renew_flag = ResponseField(CharField, desc = "续签标识")
    response.expire_time = ResponseField(CharField, desc = "到期时间")

    @classmethod
    def get_desc(cls):
        return "员工登录接口"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        token = StaffAccountServer.login(request.username, request.password)
        return token

    def fill(self, response, token):
        response.access_token = token.auth_token
        response.renew_flag = token.renew_flag
        response.expire_time = token.expire_time
        return response


class Logout(StaffAuthorizedApi):
    """注销"""
    request = with_metaclass(RequestFieldSet)
    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "员工注销接口"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        staff = self.auth_user
        StaffAccountServer.logout(staff)

    def fill(self, response):
        return response
