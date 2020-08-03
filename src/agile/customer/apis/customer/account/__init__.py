# coding=UTF-8

'''
Created on 2020年7月3日

@author: Roy
'''

from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet
from infrastructure.core.exception.business_error import BusinessError
from infrastructure.core.field.base import CharField, BooleanField

from agile.base.api import NoAuthorizedApi
from agile.customer.manager.api import CustomerAuthorizedApi
from abs.services.customer.account.manager import CustomerAccountServer
from abs.services.customer.personal.manager import CustomerServer
from abs.services.crm.tool.manager import SmsServer


class Register(NoAuthorizedApi):

    request = with_metaclass(RequestFieldSet)
    request.phone = RequestField(CharField, desc="手机号码")
    request.password = RequestField(CharField, desc="密码")
    request.code = RequestField(CharField, desc="验证码")

    response = with_metaclass(ResponseFieldSet)
    response.access_token = ResponseField(CharField, desc="访问凭证")
    response.renew_flag = ResponseField(CharField, desc="续签标识")
    response.expire_time = ResponseField(CharField, desc="到期时间")

    @classmethod
    def get_desc(cls):
        return "客户注册接口"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        if not SmsServer.check_register_code(
            request.phone,
            request.code
        ):
            raise BusinessError('验证码错误')

        if CustomerAccountServer.is_exsited(request.phone):
            raise BusinessError('账号已存在')

        customer = CustomerServer.create(
            request.phone,
        )

        token = CustomerAccountServer.create(
            customer.id,
            request.phone,
            request.password,
        )
        return token

    def fill(self, response, token):
        response.access_token = token.auth_token
        response.renew_flag = token.renew_flag
        response.expire_time = token.expire_time
        return response


class Login(NoAuthorizedApi):

    request = with_metaclass(RequestFieldSet)
    request.username = RequestField(CharField, desc="账号")
    request.password = RequestField(CharField, desc="密码")

    response = with_metaclass(ResponseFieldSet)
    response.access_token = ResponseField(CharField, desc="访问凭证")
    response.renew_flag = ResponseField(CharField, desc="续签标识")
    response.expire_time = ResponseField(CharField, desc="到期时间")

    @classmethod
    def get_desc(cls):
        return "客户登录接口"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        token = CustomerAccountServer.login(
            request.username,
            request.password
        )
        return token

    def fill(self, response, token):
        response.access_token = token.auth_token
        response.renew_flag = token.renew_flag
        response.expire_time = token.expire_time
        return response


class CodeLogin(NoAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.username = RequestField(CharField, desc="账号")
    request.verify_code = RequestField(CharField, desc="密码")

    response = with_metaclass(ResponseFieldSet)
    response.access_token = ResponseField(CharField, desc="访问凭证")
    response.renew_flag = ResponseField(CharField, desc="续签标识")
    response.expire_time = ResponseField(CharField, desc="到期时间")
    response.is_password = ResponseField(BooleanField, desc="是否有密码")

    @classmethod
    def get_desc(cls):
        return "验证码登陆"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        if not SmsServer.check_code(
                request.username,
                'login',
                request.verify_code
        ):
            raise BusinessError('验证码错误')
        account = CustomerAccountServer.get_customer_account_byusername(
            request.username
        )
        password = ''
        if account:
            token = CustomerAccountServer.account_login(
                account
            )
            password = account.password
        else:
            customer = CustomerServer.create(
                request.username,
            )
            token = CustomerAccountServer.create(
                customer.id,
                request.username,
                password,
            )
        return token, password

    def fill(self, response, token, password):
        response.is_password = True if password else False
        response.access_token = token.auth_token
        response.renew_flag = token.renew_flag
        response.expire_time = token.expire_time
        return response


class Logout(CustomerAuthorizedApi):

    request = with_metaclass(RequestFieldSet)
    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "客户注销接口"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        customer = self.auth_user
        CustomerAccountServer.logout(customer.id)

    def fill(self, response):
        return response
