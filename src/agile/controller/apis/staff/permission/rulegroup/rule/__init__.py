# coding=UTF-8

'''
Created on 2020年7月23日

@author: Roy
'''

from infrastructure.core.field.base import CharField,\
        IntField, ListField, DatetimeField, IterationField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet

from agile.controller.manager.api import StaffAuthorizedApi
from abs.services.controller.staff.manager import StaffServer
from abs.middleground.technology.permission.manager import PermissionServer


class All(StaffAuthorizedApi):
    """
    所有规则
    """
    request = with_metaclass(RequestFieldSet)

    response = with_metaclass(ResponseFieldSet)
    response.rule_list = ResponseField(
        ListField,
        desc="一级规则",
        fmt=IterationField(
            desc="规则",
            flag="children",
            fmt={
                'id': IntField(desc="编号I"),
                'platform_id': IntField(desc="平台id"),
                'name': CharField(desc="名称I"),
                'code': CharField(desc="编码"),
                'paths': CharField(desc="全编码编码"),
                'parent_id': IntField(desc="父级ID"),
                'remark': CharField(desc="备注"),
                'description': CharField(desc="描述"),
                'create_time': DatetimeField(desc="创建时间"),
                'update_time': DatetimeField(desc="创建时间"),
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
        staff_id = self.auth_user.id
        staff = StaffServer.get(staff_id)
        rule_list = PermissionServer.get_all_rule_byappkey(
            staff.company.permission_key
        )
        return rule_list

    def fill(self, response, rule_list):
        response.rule_list = rule_list
        return response
