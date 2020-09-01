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

from agile.crm.manager.api import StaffAuthorizedApi
from abs.middleware.config import config_middleware
from abs.middleground.technology.permission.manager import PermissionServer


class Add(StaffAuthorizedApi):
    """
    添加组织
    """
    request = with_metaclass(RequestFieldSet)
    request.organization_info = RequestField(
        DictField,
        desc = "组织详情",
        conf = {
            'position_id_list': ListField(
                desc = "身份列表",
                fmt = IntField(desc = "身份id")
            ),
            'parent_id': IntField(desc = "上级组织id"),
            'name': CharField(desc = "组织名称"),
            'description': CharField(desc = "描述"),
            'remark': CharField(desc = "备注"),
        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.organization_id = ResponseField(IntField, desc = "组织Id")

    @classmethod
    def get_desc(cls):
        return "添加组织"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        appkey = config_middleware.get_value("common", "crm_appkey")
        organization = PermissionServer.add_organization(
            appkey = appkey,
            **request.organization_info
        )
        return organization

    def fill(self, response, organization):
        response.organization_id = organization.id
        return response


class All(StaffAuthorizedApi):
    """
    所有组织
    """
    request = with_metaclass(RequestFieldSet)

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(
        ListField,
        desc = "组织列表",
        fmt = IterationField(
            desc = "组织详情",
            flag = "children",
            fmt = {
                "id": IntField(desc = "id"),
                "name": CharField(desc = "名称"),
                "remark": CharField(desc = "备注"),
                "description": CharField(desc = "描述"),
                "parent_id": IntField(desc = "父级ID"),
                "update_time": DatetimeField(desc = "更新时间"),
                "create_time": DatetimeField(desc = "创建时间"),
            }
        )
    )

    @classmethod
    def get_desc(cls):
        return "所有组织"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        appkey = config_middleware.get_value("common", "crm_appkey")
        organization_list = PermissionServer.get_all_organization_byappkey(
            appkey
        )
        return organization_list

    def fill(self, response, organization_list):
        response.data_list = organization_list
        return response


class Get(StaffAuthorizedApi):
    """
    获取组织接口
    """
    request = with_metaclass(RequestFieldSet)
    request.organization_id = RequestField(IntField, desc = "组织id")

    response = with_metaclass(ResponseFieldSet)
    response.organization_info = ResponseField(
        DictField,
        desc = "组织详情",
        conf = {
            "id": IntField(desc = "名称"),
            "name": CharField(desc = "名称"),
            "description": CharField(desc = "描述"),
            "remark": CharField(desc = "备注"),
            "parent_id": IntField(desc = "父级ID"),
            'position_list':ListField(
                desc = "身份列表",
                fmt = DictField(
                    desc = "身份详情",
                    conf = {
                        "id": IntField(desc = "身份id"),
                        "name": CharField(desc = "身份名称"),
                    }
                )
            ),
            "create_time": DatetimeField(desc = "创建时间"),
        }
    )

    @classmethod
    def get_desc(cls):
        return "获取组织详情接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        organization = PermissionServer.get_organization(
            request.organization_id
        )
        return organization

    def fill(self, response, organization):
        response.organization_info = {
            'id': organization.id,
            'name': organization.name,
            'parent_id': organization.parent_id,
            'description': organization.description,
            'remark': organization.remark,
            'position_list':[{
                "id":position.id,
                "name":position.name
             } for position in organization.position_list],
            'create_time': organization.create_time,
        }
        return response


class Update(StaffAuthorizedApi):
    """
    修改组织信息
    """
    request = with_metaclass(RequestFieldSet)
    request.organization_id = RequestField(IntField, desc = "组织id")
    request.update_info = RequestField(
        DictField,
        desc = "组织修改详情",
        conf = {
            'position_id_list': ListField(
                desc = "身份列表",
                fmt = IntField(desc = "身份id")
            ),
            'name': CharField(desc = "名称", is_required = False),
            'description': CharField(desc = "描述", is_required = False),
            'parent_id': IntField(desc = "父级ID", is_required = False),
            'remark': CharField(desc = "备注", is_required = False),
        }
    )

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "修改组织信息"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        PermissionServer.update_organization(
            request.organization_id,
            **request.update_info
        )

    def fill(self, response):
        return response


class Remove(StaffAuthorizedApi):
    """
    删除组织信息
    """
    request = with_metaclass(RequestFieldSet)
    request.organization_id = RequestField(IntField, desc = "组织id")

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "删除组织"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        PermissionServer.remove_organization(
            request.organization_id
        )

    def fill(self, response):
        return response
