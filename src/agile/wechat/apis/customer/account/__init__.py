# coding=UTF-8

from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet
from infrastructure.core.exception.business_error import BusinessError
from infrastructure.core.field.base import CharField, DictField
from abs.middleware.login import login_middleware

from agile.base.api import NoAuthorizedApi
from abs.services.customer.account.utils.constant import CategoryTypes
from abs.services.customer.account.manager import TripartiteServer
from abs.services.customer.account.manager import CustomerAccountServer
from abs.services.customer.personal.manager import CustomerServer
from abs.services.crm.tool.manager import SmsServer
from agile.wechat.manager.api import WechatAuthorizedApi


class AutoLogin(NoAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.code = RequestField(CharField, desc='code')

    response = with_metaclass(ResponseFieldSet)
    response.access_token = ResponseField(CharField, desc="用户访问令牌")
    response.renew_flag = ResponseField(CharField, desc="续签访问令牌标识")

    @classmethod
    def get_desc(cls):
        return "自动登录接口"

    @classmethod
    def get_author(cls):
        return "xyc"

    def execute(self, request):
        openid = login_middleware.wechat_login(request.code).get('openid')
        tripartite = TripartiteServer.get_byopenid(openid, CategoryTypes.WECHAT)
        if tripartite:
            token = CustomerAccountServer.account_login(
                tripartite.customer_account
            )
            auth_token = token.auth_token
            renew_flag = token.renew_flag
        else:
            auth_token = ''
            renew_flag = ''
        return auth_token, renew_flag

    def fill(self, response, auth_token, renew_flag):
        response.access_token = auth_token
        response.renew_flag = renew_flag
        return response


class PhoneRegister(NoAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.phone = RequestField(CharField, desc='手机号')
    request.verify_code = RequestField(CharField, desc='手机验证码')
    request.code = RequestField(CharField, desc='微信code')

    response = with_metaclass(ResponseFieldSet)
    response.access_token = ResponseField(CharField, desc="用户访问令牌")
    response.renew_flag = ResponseField(CharField, desc="续签访问令牌标识")

    @classmethod
    def get_desc(cls):
        return "手机验证码注册接口"

    @classmethod
    def get_author(cls):
        return "xyc"

    def execute(self, request):
        openid = login_middleware.wechat_login(request.code).get('openid')
        tripartite = TripartiteServer.get_byopenid(openid, CategoryTypes.WECHAT)
        if tripartite:
            raise BusinessError('微信已被绑定')
        account = CustomerAccountServer.get_customer_account_byusername(
            request.phone
        )
        if account:
            if TripartiteServer.search_all(
                    customer_account=account,
                    category=CategoryTypes.WECHAT
            ):
                raise BusinessError('该手机号账号已绑定其他微信')

        if not SmsServer.check_code(
            request.phone,
            "wechat_register",
            request.verify_code
        ):
            raise BusinessError('验证码错误')
        if account:
            token = CustomerAccountServer.account_login(
                account
            )
        else:
            customer = CustomerServer.create(
                request.phone,
            )
            token = CustomerAccountServer.create(
                customer.id,
                request.phone,
                '',
            )
            account = CustomerAccountServer.get_customer_account_byusername(
                request.phone
            )
        TripartiteServer.create(
            customer_account=account,
            category=CategoryTypes.WECHAT,
            openid=openid
        )
        return token

    def fill(self, response, token):
        response.access_token = token.auth_token
        response.renew_flag = token.renew_flag
        return response


class WechatRegister(NoAuthorizedApi):
    """获取用户微信手机号"""
    request = with_metaclass(RequestFieldSet)
    request.data_info = RequestField(DictField, desc='微信信息', conf={
        'encrypted_data': CharField(desc="encryptedData"),
        'iv': CharField(desc="iv"),
        'code': CharField(desc="jsCode")
    })

    response = with_metaclass(ResponseFieldSet)
    response.access_token = ResponseField(CharField, desc="用户访问令牌")
    response.renew_flag = ResponseField(CharField, desc="续签访问令牌标识")

    @classmethod
    def get_desc(cls):
        return "用户信息修改接口"

    @classmethod
    def get_author(cls):
        return "xyc"

    def execute(self, request):
        encrypted_data = request.data_info['encrypted_data']
        iv = request.data_info['iv']
        result = login_middleware.wechat_login(request.data_info['code'])
        openid = result.get('openid')
        session_key = result.get('session_key')
        data = login_middleware.get_wechat_info(encrypted_data, session_key, iv)
        phone = data.get('purePhoneNumber')
        account = CustomerAccountServer.get_customer_account_byusername(
            phone
        )

        if account:
            if TripartiteServer.search_all(
                    customer_account=account,
                    category=CategoryTypes.WECHAT
            ):
                raise BusinessError('该手机号账号已绑定其他微信')

        if account:
            token = CustomerAccountServer.account_login(
                account
            )
        else:
            customer = CustomerServer.create(
                phone
            )
            token = CustomerAccountServer.create(
                customer.id,
                phone,
                '',
            )
            account = CustomerAccountServer.get_customer_account_byusername(
                phone
            )
        TripartiteServer.create(
            customer_account=account,
            category=CategoryTypes.WECHAT,
            openid=openid
        )
        return token

    def fill(self, response, token):
        response.access_token = token.auth_token
        response.renew_flag = token.renew_flag
        return response


class Unbind(WechatAuthorizedApi):
    request = with_metaclass(RequestFieldSet)

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "解绑"

    @classmethod
    def get_author(cls):
        return "xyc"

    def execute(self, request):
        account = CustomerAccountServer.get(self.auth_user.id)
        TripartiteServer.search_all(
            customer_account=account,
            category=CategoryTypes.WECHAT
        ).delete()

    def fill(self, response):
        return response
