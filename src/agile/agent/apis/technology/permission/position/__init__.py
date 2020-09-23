# coding=UTF-8

'''
Created on 2020年7月23日

@author: Roy
'''
import json
from infrastructure.core.field.base import CharField, DictField, \
        IntField, ListField, DatetimeField, IterationField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet
from infrastructure.utils.common.jsontools import CJsonEncoder

from agile.base.api import NoAuthorizedApi
from agile.agent.manager.api import AgentStaffAuthorizedApi
from abs.middleground.technology.permission.manager import PermissionServer


class Add(AgentStaffAuthorizedApi):
    """
    添加身份
    """
    request = with_metaclass(RequestFieldSet)
    request.position_info = RequestField(
        DictField,
        desc = "身份详情",
        conf = {
            'rule_group_id': IntField(desc = "权限组id"),
            'parent_id': IntField(desc = "上级身份id"),
            'description': CharField(desc = "描述"),
            'name': CharField(desc = "身份名称"),
            'remark': CharField(desc = "备注"),
        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.position_id = ResponseField(IntField, desc = "身份Id")

    @classmethod
    def get_desc(cls):
        return "添加身份"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        agent = self.auth_user.company
        position = PermissionServer.add_position(
            appkey = agent.permission_key,
            **request.position_info
        )
        return position

    def fill(self, response, position):
        response.position_id = position.id
        return response


class All(AgentStaffAuthorizedApi):
    """
    所有身份
    """
    request = with_metaclass(RequestFieldSet)

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(
        ListField,
        desc = "身份列表",
        fmt = DictField(
            desc = "身份详情",
            conf = {
                "id": IntField(desc = "ID"),
                "name": CharField(desc = "名称"),
                "description": CharField(desc = "描述"),
                "remark": CharField(desc = "备注"),
            }
        )
    )

    @classmethod
    def get_desc(cls):
        return "所有身份"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        agent = self.auth_user.company
        position_list = PermissionServer.get_all_position_byappkey(
            agent.permission_key
        )
        return position_list

    def fill(self, response, position_list):
        response.data_list = [{
            'id': position.id,
            'name': position.name,
            'description': position.description,
            'remark': position.remark,
        } for position in position_list]
        return response


class Tree(AgentStaffAuthorizedApi):
    """
    树状所有身份
    """
    request = with_metaclass(RequestFieldSet)

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(
        ListField,
        desc = "身份列表",
        fmt = IterationField(
            desc = "身份详情",
            flag = "children",
            fmt = {
                "id": IntField(desc = "名称"),
                "name": CharField(desc = "名称"),
                "remark": CharField(desc = "备注"),
                "description": CharField(desc = "描述"),
                "parent_id": IntField(desc = "父级ID"),
                "rule_group_id": IntField(desc = "权限组ID"),
                "rule_group_name": CharField(desc = "权限组名称"),
                "create_time": DatetimeField(desc = "创建时间"),
                "update_time": DatetimeField(desc = "更新时间"),
            }
        )
    )

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        agent = self.auth_user.company
        position_list = PermissionServer.get_tree_position_byappkey(
            agent.permission_key
        )
        return position_list

    def fill(self, response, position_list):
        response.data_list = position_list
        return response


class Get(AgentStaffAuthorizedApi):
    """
    获取身份接口
    """
    request = with_metaclass(RequestFieldSet)
    request.position_id = RequestField(IntField, desc = "身份id")

    response = with_metaclass(ResponseFieldSet)
    response.position_info = ResponseField(
        DictField,
        desc = "身份详情",
        conf = {
            "id": IntField(desc = "名称"),
            "name": CharField(desc = "名称"),
            "description": CharField(desc = "描述"),
            "remark": CharField(desc = "备注"),
            "parent_id": IntField(desc = "父级ID"),
            "rule_group_name": CharField(desc = "权限组名称"),
            "rule_group_id": IntField(desc = "权限组ID"),
            "create_time": DatetimeField(desc = "创建时间"),
        }
    )

    @classmethod
    def get_desc(cls):
        return "获取身份详情接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        position = PermissionServer.get_position(
            request.position_id
        )
        return position

    def fill(self, response, position):
        response.position_info = {
            'id': position.id,
            'name': position.name,
            'parent_id': position.parent_id,
            'rule_group_name': position.rule_group.name,
            'position_id': position.position_id,
            'description': position.description,
            'remark': position.remark,
            'create_time': position.create_time,
        }
        return response


class Update(AgentStaffAuthorizedApi):
    """
    修改身份信息
    """
    request = with_metaclass(RequestFieldSet)
    request.position_id = RequestField(IntField, desc = "身份id")
    request.update_info = RequestField(
        DictField,
        desc = "身份修改详情",
        conf = {
            'rule_group_id': IntField(desc = "权限组id", is_required = False),
            'parent_id': IntField(desc = "上级身份id"),
            'description': CharField(desc = "描述"),
            'name': CharField(desc = "身份名称"),
            'remark': CharField(desc = "备注", is_required = False),
        }
    )

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "修改身份信息"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        PermissionServer.update_position(
            request.position_id,
            **request.update_info
        )

    def fill(self, response):
        return response


class Remove(AgentStaffAuthorizedApi):
    """
    删除身份信息
    """
    request = with_metaclass(RequestFieldSet)
    request.position_id = RequestField(IntField, desc = "身份id")

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "删除身份"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        PermissionServer.remove_position(
            request.position_id
        )

    def fill(self, response):
        return response
