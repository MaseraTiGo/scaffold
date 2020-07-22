# coding=UTF-8

'''
Created on 2020年7月5日

@author: Roy
'''

from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet
from infrastructure.core.field.base import CharField

from agile.base.api import NoAuthorizedApi
from agile.customer.manager.api import CustomerAuthorizedApi
from abs.services.customer.account.manager import CustomerAccountServer


class Forget(NoAuthorizedApi):

    request = with_metaclass(RequestFieldSet)
    request.phone = RequestField(CharField, desc="手机号码")
    request.code = RequestField(CharField, desc="验证码")
    request.password = RequestField(CharField, desc="密码")

    response = with_metaclass(ResponseFieldSet)
    response.access_token = ResponseField(CharField, desc="访问凭证")
    response.renew_flag = ResponseField(CharField, desc="续签标识")
    response.expire_time = ResponseField(CharField, desc="到期时间")

    @classmethod
    def get_desc(cls):
        return "客户忘记密码接口"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        token = CustomerAccountServer.forget_password(
            phone=request.phone,
            code=request.code,
            new_password=request.password
        )
        return token

    def fill(self, response, token):
        response.access_token = token.auth_token
        response.renew_flag = token.renew_flag
        response.expire_time = token.expire_time
        return response


class Modify(CustomerAuthorizedApi):

    request = with_metaclass(RequestFieldSet)
    request.old_password = RequestField(CharField, desc="老密码")
    request.new_password = RequestField(CharField, desc="新密码")

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "客户修改密码接口"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        CustomerAccountServer.modify_password(
            self.auth_user.id,
            old_password=request.old_password,
            new_password=request.new_password
        )

    def fill(self, response, token):
        return response
