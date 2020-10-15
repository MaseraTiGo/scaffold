# coding=UTF-8

'''
Created on 2016年7月23日

@author: Roy
'''
import hashlib
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet
from infrastructure.core.field.base import CharField, IntField, DictField, ListField

from agile.base.api import NoAuthorizedApi
from agile.agent.manager.api import AgentStaffAuthorizedApi
from abs.services.agent.account.manager import AgentStaffAccountServer
from abs.services.agent.agent.manager import AgentStaffServer


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
    response.rule_codes = ResponseField(ListField, desc = "rule codes",
                                       fmt = CharField(desc="rule codes"))

    @classmethod
    def get_desc(cls):
        return "员工登录接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        token = AgentStaffAccountServer.login(
            request.username,
            request.password
        )
        user_id = token.user_id
        codes = AgentStaffAccountServer.hung_rule_codes(user_id=user_id)
        return token, codes

    def fill(self, response, token, codes):
        response.access_token = token.auth_token
        response.renew_flag = token.renew_flag
        response.expire_time = token.expire_time
        response.rule_codes = codes
        return response


class Logout(AgentStaffAuthorizedApi):
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
        AgentStaffAccountServer.logout(self._token.auth_token)

    def fill(self, response):
        return response


class Add(AgentStaffAuthorizedApi):
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
        agent_staff = AgentStaffServer.get(request.staff_id)
        check_account = AgentStaffAccountServer.is_exsited(
            request.account_info["username"]
        )
        if check_account:
            AgentStaffAccountServer.update(
                agent_staff.id,
                **request.account_info
            )
        else:
            AgentStaffAccountServer.create(
                agent_staff.id,
                request.account_info["username"],
                request.account_info["password"] if \
                "password" in request.account_info else \
                hashlib.md5("123456".encode('utf8')).hexdigest()
            )

    def fill(self, response):
        return response
