# coding=UTF-8

'''
Created on 2016年7月23日

@author: Roy
'''

from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet
from infrastructure.core.field.base import CharField, DatetimeField,\
        DictField

from agile.base.api import NoAuthorizedApi
from abs.middleground.business.account.utils.constant import StatusTypes
from agile.controller.manager.api import StaffAuthorizedApi
from abs.services.controller.account.manager import StaffAccountServer


class Login(NoAuthorizedApi):
    """
    账号密码登录接口
    """
    request = with_metaclass(RequestFieldSet)
    request.username = RequestField(CharField, desc="账号")
    request.password = RequestField(CharField, desc="密码")
    request._ip = RequestField(CharField, desc="ip地址")

    response = with_metaclass(ResponseFieldSet)
    response.access_token = ResponseField(CharField, desc="访问凭证")
    response.renew_flag = ResponseField(CharField, desc="续签标识")
    response.expire_time = ResponseField(CharField, desc="到期时间")

    @classmethod
    def get_desc(cls):
        return "账号密码登录接口"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        token = StaffAccountServer.login(
            request.username,
            request.password,
            request._ip,
        )
        return token

    def fill(self, response, token):
        response.access_token = token.auth_token
        response.renew_flag = token.renew_flag
        response.expire_time = token.expire_time
        return response


class Logout(StaffAuthorizedApi):
    """
    注销登录接口
    """
    request = with_metaclass(RequestFieldSet)
    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "员工注销接口"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        StaffAccountServer.logout(self._token.auth_token)

    def fill(self, response):
        return response


class Get(StaffAuthorizedApi):
    """
    获取账号信息接口
    """
    request = with_metaclass(RequestFieldSet)

    response = with_metaclass(ResponseFieldSet)
    response.account_info = ResponseField(
        DictField,
        desc="账号信息",
        conf={
            'username': CharField(desc="账号"),
            'nick': CharField(desc="昵称"),
            'head_url': CharField(desc="头像"),
            'last_login_time': DatetimeField(desc="最后登录时间"),
            'last_login_ip': CharField(desc="最后登录ip"),
            'register_ip': CharField(desc="注册ip"),
            'status': CharField(
                desc="状态",
                is_required=False,
                choices=StatusTypes.CHOICES
            ),
            'update_time': DatetimeField(desc="更新时间"),
            'create_time': DatetimeField(desc="创建时间"),
        }
    )

    @classmethod
    def get_desc(cls):
        return "获取账号信息接口"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        account = StaffAccountServer.get(self.auth_user.id)
        return account

    def fill(self, response, account):
        response.account_info = {
            "username": account.username,
            "nick": account.nick,
            "head_url": account.head_url,
            "last_login_time": account.last_login_time,
            "last_login_ip": account.last_login_ip,
            "register_ip": account.register_ip,
            "status": account.status,
            "update_time": account.update_time,
            "create_time": account.create_time,
        }
        return response


class Update(StaffAuthorizedApi):
    """
    更新账号信息接口
    """
    request = with_metaclass(RequestFieldSet)
    request.update_info = RequestField(
        DictField,
        desc="员工修改详情",
        conf={
            'nick': CharField(desc="昵称", is_required=False),
            'head_url': CharField(desc="头像", is_required=False),
            'statue': CharField(
                desc="状态",
                is_required=False,
                choices=StatusTypes.CHOICES
            ),
        }
    )
    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "更新账号信息接口"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        StaffAccountServer.update(
            self.auth_user.id,
            **request.update_info,
        )

    def fill(self, response):
        return response
