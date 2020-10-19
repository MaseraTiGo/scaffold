# coding=UTF-8

'''
Created on 2020年7月3日

@author: Roy
'''

from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet
from infrastructure.core.exception.business_error import BusinessError
from infrastructure.core.field.base import CharField, BooleanField, ListField, IntField

from agile.base.api import NoAuthorizedApi
from agile.customer.manager.api import CustomerAuthorizedApi
from abs.services.customer.account.manager import CustomerAccountServer
from abs.services.customer.personal.manager import CustomerServer
from abs.services.crm.tool.manager import SmsServer
from abs.services.customer.personal.manager import CollectionRecordServer
from abs.middleware.login import login_app_middleware
from abs.services.customer.account.manager import TripartiteServer
from abs.services.customer.account.utils.constant import CategoryTypes


class Register(NoAuthorizedApi):

    request = with_metaclass(RequestFieldSet)
    request.phone = RequestField(CharField, desc = "手机号码")
    request.password = RequestField(CharField, desc = "密码")
    request.code = RequestField(CharField, desc = "验证码")
    request.unique_code = RequestField(CharField, desc = "设备唯一编码")
    request._clientType = RequestField(CharField, desc = "登陆手机系统类型")

    response = with_metaclass(ResponseFieldSet)
    response.access_token = ResponseField(CharField, desc = "访问凭证")
    response.renew_flag = ResponseField(CharField, desc = "续签标识")
    response.expire_time = ResponseField(CharField, desc = "到期时间")

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
        CustomerAccountServer.update_phone_unique(
            customer.id,
            request.unique_code,
            request._clientType
        )
        return token

    def fill(self, response, token):
        response.access_token = token.auth_token
        response.renew_flag = token.renew_flag
        response.expire_time = token.expire_time
        return response


class Login(NoAuthorizedApi):

    request = with_metaclass(RequestFieldSet)
    request.username = RequestField(CharField, desc = "账号")
    request.password = RequestField(CharField, desc = "密码")
    request.unique_code = RequestField(CharField, desc = "设备唯一编码")
    request._clientType = RequestField(CharField, desc = "登陆手机系统类型")

    response = with_metaclass(ResponseFieldSet)
    response.access_token = ResponseField(CharField, desc = "访问凭证")
    response.renew_flag = ResponseField(CharField, desc = "续签标识")
    response.expire_time = ResponseField(CharField, desc = "到期时间")
    response.goods_ids = ResponseField(ListField,
                                    desc="收藏商品id列表",
                                    fmt=IntField(desc="商品id"))

    @classmethod
    def get_desc(cls):
        return "客户登录接口"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        token = CustomerAccountServer.login(
            request.username,
            request.password,
        )
        CustomerAccountServer.update_phone_unique(
            token.user_id,
            request.unique_code,
            request._clientType
        )
        # 查询用户收藏商品id
        goods_ids = []
        customer = CustomerServer.get(token.user_id)
        if customer:
            cr_qs = CollectionRecordServer.search_all(**{'customer': customer, 'is_delete': False})
            goods_ids = [collection.goods_id for collection in cr_qs]
            goods_ids = list(set(goods_ids))
        return token, goods_ids

    def fill(self, response, token, goods_ids):
        response.access_token = token.auth_token
        response.renew_flag = token.renew_flag
        response.expire_time = token.expire_time
        response.goods_ids = goods_ids
        return response


class CodeLogin(NoAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.username = RequestField(CharField, desc = "账号")
    request.verify_code = RequestField(CharField, desc = "密码")
    request.unique_code = RequestField(CharField, desc = "设备唯一编码")
    request._clientType = RequestField(CharField, desc = "登陆手机系统类型")

    response = with_metaclass(ResponseFieldSet)
    response.access_token = ResponseField(CharField, desc = "访问凭证")
    response.renew_flag = ResponseField(CharField, desc = "续签标识")
    response.expire_time = ResponseField(CharField, desc = "到期时间")
    response.is_password = ResponseField(BooleanField, desc = "是否有密码")
    response.goods_ids = ResponseField(ListField,
                                       desc="收藏商品id列表",
                                       fmt=IntField(desc="商品id"))

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
                account,
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
        CustomerAccountServer.update_phone_unique(
            token.user_id,
            request.unique_code,
            request._clientType
        )

        # 查询用户收藏商品id
        goods_ids = []
        customer = CustomerServer.get_customer_obj(request.username)
        if customer:
            cr_qs = CollectionRecordServer.search_all(**{'customer': customer, 'is_delete': False})
            goods_ids = [collection.goods_id for collection in cr_qs]
            goods_ids = list(set(goods_ids))
        return token, password, goods_ids

    def fill(self, response, token, password, goods_ids):
        response.is_password = True if password else False
        response.access_token = token.auth_token
        response.renew_flag = token.renew_flag
        response.expire_time = token.expire_time
        response.goods_ids = goods_ids
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
        auth_token = self._token.auth_token
        CustomerAccountServer.logout(
            customer.id, auth_token
        )

    def fill(self, response):
        return response


class WeChatLogin(NoAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.open_id = RequestField(CharField, desc='用户openid')
    request.access_token = RequestField(CharField, desc='access_token')

    response = with_metaclass(ResponseFieldSet)
    response.access_token = ResponseField(CharField, desc="用户访问令牌")
    response.renew_flag = ResponseField(CharField, desc="续签访问令牌标识")
    response.goods_ids = ResponseField(ListField,
                                       desc="收藏商品id列表",
                                       fmt=IntField(desc="商品id"))

    @classmethod
    def get_desc(cls):
        return "第三方微信登录接口"

    @classmethod
    def get_author(cls):
        return "djd"

    def execute(self, request):
        print('=====================customer wechat login=========================')
        # openid, _ = login_app_middleware.wechat_login(request.code)
        openid = request.open_id
        tripartite = TripartiteServer.get_byopenid(openid, CategoryTypes.WECHAT_APP)
        if tripartite:
            token = CustomerAccountServer.account_login(
                tripartite.customer_account
            )
            auth_token = token.auth_token
            renew_flag = token.renew_flag
        else:
            auth_token = ''
            renew_flag = ''

        goods_ids = []
        if auth_token:
            # 查询用户收藏商品id
            customer = CustomerServer.get(tripartite.customer_account.role_id)
            if customer:
                cr_qs = CollectionRecordServer.search_all(**{'customer': customer, 'is_delete': False})
                goods_ids = [collection.goods_id for collection in cr_qs]
                goods_ids = list(set(goods_ids))
        return auth_token, renew_flag, goods_ids

    def fill(self, response, auth_token, renew_flag, goods_ids):
        response.access_token = auth_token
        response.renew_flag = renew_flag
        response.goods_ids = goods_ids
        return response


class WechatRegister(NoAuthorizedApi):

    request = with_metaclass(RequestFieldSet)
    request.phone = RequestField(CharField, desc="手机号码")
    request.verify_code = RequestField(CharField, desc='手机验证码')
    request.open_id = RequestField(CharField, desc="用户openid")
    request.access_token = RequestField(CharField, desc="access_token")
    request.unique_code = RequestField(CharField, desc="设备唯一编码")
    request._clientType = RequestField(CharField, desc="登陆手机系统类型")

    response = with_metaclass(ResponseFieldSet)
    response.access_token = ResponseField(CharField, desc="访问凭证")
    response.renew_flag = ResponseField(CharField, desc="续签标识")
    response.expire_time = ResponseField(CharField, desc="到期时间")

    @classmethod
    def get_desc(cls):
        return "wechat绑定手机号"

    @classmethod
    def get_author(cls):
        return "djd"

    def execute(self, request):
        print('=====================customer wechat register=========================')
        # if CustomerAccountServer.is_exsited(request.phone):
        #     raise BusinessError('该手机号已被绑定')
        if not SmsServer.check_code(
            request.phone,
            "bindwechat",
            request.verify_code
        ):
            raise BusinessError('验证码错误')
        customer_account = CustomerAccountServer.get_customer_account_byusername(request.phone)
        if customer_account:
            tripartite_qs = TripartiteServer.search_all(
                customer_account=customer_account,
                category=CategoryTypes.WECHAT_APP
            )
            if tripartite_qs.count() > 0:
                tripartite = tripartite_qs[0]
                if tripartite.openid != request.open_id:
                    raise BusinessError('该手机号账号已绑定其他微信')
            else:
                TripartiteServer.create(**{
                    'customer_account': customer_account,
                    'openid': request.open_id,
                    'category': CategoryTypes.WECHAT_APP,
                })
                token = CustomerAccountServer.account_login(customer_account)
                return token

        user_wechat_info = login_app_middleware.user_info(request.access_token, request.open_id)

        base_info = {}
        if user_wechat_info:
            base_info.update({'head_url': user_wechat_info.get('headimgurl', ''),
                             'nick': user_wechat_info.get('nickname', ''),
                              })
        customer = CustomerServer.create(
            request.phone,
            **base_info
        )

        token = CustomerAccountServer.create(
            customer.id,
            request.phone,
            '',

        )
        CustomerAccountServer.update_phone_unique(
            customer.id,
            request.unique_code,
            request._clientType
        )
        # add head_url, nick to customer_account table
        customer_account = CustomerAccountServer.get_customer_account_by_id(customer.id)
        customer_account.update(**base_info)
        TripartiteServer.create(**{
            'customer_account': customer_account,
            'openid': request.open_id,
            'category': CategoryTypes.WECHAT_APP,
        })
        return token

    def fill(self, response, token):
        response.access_token = token.auth_token
        response.renew_flag = token.renew_flag
        response.expire_time = token.expire_time
        return response


class QQLogin(NoAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.open_id = RequestField(CharField, desc='qq用户的openid')

    response = with_metaclass(ResponseFieldSet)
    response.access_token = ResponseField(CharField, desc="用户访问令牌")
    response.renew_flag = ResponseField(CharField, desc="续签访问令牌标识")
    response.goods_ids = ResponseField(ListField,
                                       desc="收藏商品id列表",
                                       fmt=IntField(desc="商品id"))

    @classmethod
    def get_desc(cls):
        return "第三方QQ登录接口"

    @classmethod
    def get_author(cls):
        return "djd"

    def execute(self, request):
        # todo: not implement
        openid, _ = login_app_middleware.wechat_login(request.code)

        tripartite = TripartiteServer.get_byopenid(openid, CategoryTypes.QQ)
        if tripartite:
            token = CustomerAccountServer.account_login(
                tripartite.customer_account
            )
            auth_token = token.auth_token
            renew_flag = token.renew_flag
        else:
            auth_token = ''
            renew_flag = ''

        # 查询用户收藏商品id
        goods_ids = []
        if auth_token:
            customer = CustomerServer.get(tripartite.customer_account.role_id)
            if customer:
                cr_qs = CollectionRecordServer.search_all(**{'customer': customer, 'is_delete': False})
                goods_ids = [collection.goods_id for collection in cr_qs]
                goods_ids = list(set(goods_ids))
        return auth_token, renew_flag, goods_ids

    def fill(self, response, auth_token, renew_flag, goods_ids):
        response.access_token = auth_token
        response.renew_flag = renew_flag
        response.goods_ids = goods_ids
        return response