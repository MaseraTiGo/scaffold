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

from agile.base.api import NoAuthorizedApi
from agile.customer.manager.api import CustomerAuthorizedApi
from abs.service.customer.manager import CustomerServer, CustomerAccountServer



class Phone(NoAuthorizedApi):

    request = with_metaclass(RequestFieldSet)
    request.number = RequestField(CharField, desc = "手机号码")

    response = with_metaclass(ResponseFieldSet)
    response.code = ResponseField(CharField, desc = "手机验证码")

    @classmethod
    def get_desc(cls):
        return "获取登录手机验证码"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        return CustomerAccountServer.get_phone_verification_code(request.number)

    def fill(self, response, code):
        response.code = code
        return response



class Image(NoAuthorizedApi):

    request = with_metaclass(RequestFieldSet)

    response = with_metaclass(ResponseFieldSet)
    response.code = ResponseField(CharField, desc = "图片验证码")

    @classmethod
    def get_desc(cls):
        return "获取登录图片验证码"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        return CustomerAccountServer.get_image_verification_code()

    def fill(self, response, code):
        response.code = code
        return response
