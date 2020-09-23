# coding=UTF-8

'''
Created on 2020年7月23日

@author: Roy
'''

from infrastructure.core.field.base import CharField, DictField, \
        IntField, ListField, DatetimeField, IterationField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet

from agile.agent.manager.api import AgentStaffAuthorizedApi
from abs.middleground.technology.permission.manager import PermissionServer


class All(AgentStaffAuthorizedApi):
    """
    所有规则
    """
    request = with_metaclass(RequestFieldSet)

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(
        ListField,
        desc = "一级规则",
        fmt = IterationField(
            desc = "规则",
            flag = "children",
            fmt = {
                'id': IntField(desc = "编号I"),
                'platform_id': IntField(desc = "平台id"),
                'name': CharField(desc = "名称I"),
                'code': CharField(desc = "编码"),
                'parent_id': IntField(desc = "父级ID"),
                'remark': CharField(desc = "备注"),
                'description': CharField(desc = "描述"),
                'create_time': DatetimeField(desc = "创建时间"),
            }
        )
    )


    @classmethod
    def get_desc(cls):
        return "所有规则"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        agent = self.auth_user.company
        authorization = PermissionServer.get_authorization_byappkey(
            agent.permission_key
        )
        rule_list = PermissionServer.get_all_rule_byplatform(
            authorization.platform.id
        )
        return rule_list

    def fill(self, response, rule_list):
        response.data_list = rule_list
        return response
