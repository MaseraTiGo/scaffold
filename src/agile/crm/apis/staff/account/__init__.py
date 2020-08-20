# coding=UTF-8

'''
Created on 2016年7月23日

@author: Roy
'''
import hashlib
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet
from infrastructure.core.field.base import CharField, IntField, DictField

from agile.base.api import NoAuthorizedApi
from agile.crm.manager.api import StaffAuthorizedApi
from abs.services.crm.account.manager import StaffAccountServer
from abs.services.crm.staff.manager import StaffServer


class Login(NoAuthorizedApi):
    """
    员工登录接口
    """
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
        token = StaffAccountServer.login(
            request.username,
            request.password
        )
        return token

    def fill(self, response, token):
        response.access_token = token.auth_token
        response.renew_flag = token.renew_flag
        response.expire_time = token.expire_time
        return response


class Logout(StaffAuthorizedApi):
    """
    注销
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
        staff = self.auth_user
        StaffAccountServer.logout(self._token.auth_token)

    def fill(self, response):
        return response


class Add(StaffAuthorizedApi):
    """
    创建账号
    """
    request = with_metaclass(RequestFieldSet)
    request.staff_id = RequestField(IntField, desc = "员工id")
    request.account_info = RequestField(
        DictField,
        desc = "联系人账号信息",
        conf = {
            'username': CharField(desc = "账号"),
            'password': CharField(desc = "密码", is_required = False),
            'status': CharField(desc = "账号状态"),
        }
    )


    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "员工添加账号接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        staff = StaffServer.get(request.staff_id)
        check_account = StaffAccountServer.is_exsited(
            request.account_info["username"]
        )
        if check_account:
            StaffAccountServer.update(
                staff.id,
                **request.account_info
            )
        else:
            StaffAccountServer.create(
                staff.id,
                request.account_info["username"],
                request.account_info["password"] if \
                "password" in request.account_info else \
                hashlib.md5("123456".encode('utf8')).hexdigest()
            )

    def fill(self, response):
        return response
