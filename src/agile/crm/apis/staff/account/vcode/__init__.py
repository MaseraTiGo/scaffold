# coding=UTF-8

'''
Created on 2016年7月23日

@author: Roy
'''

from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet
from infrastructure.core.field.base import CharField

from agile.base.api import NoAuthorizedApi
from abs.services.crm.account.manager import StaffAccountServer


class Phone(NoAuthorizedApi):

    request = with_metaclass(RequestFieldSet)
    request.number = RequestField(CharField, desc="手机号码")

    response = with_metaclass(ResponseFieldSet)
    response.code = ResponseField(CharField, desc="手机验证码")

    @classmethod
    def get_desc(cls):
        return "获取登录手机验证码"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        return '123456'

    def fill(self, response, code):
        response.code = code
        return response


class Image(NoAuthorizedApi):

    request = with_metaclass(RequestFieldSet)

    response = with_metaclass(ResponseFieldSet)
    response.code = ResponseField(CharField, desc="图片验证码")

    @classmethod
    def get_desc(cls):
        return "获取登录图片验证码"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        return StaffAccountServer.get_image_verification_code()

    def fill(self, response, code):
        response.code = code
        return response
