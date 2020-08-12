# coding=UTF-8

'''
Created on 2020年7月23日

@author: Roy
'''

from infrastructure.core.field.base import CharField, DictField, \
        IntField, ListField, DatetimeField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet

from agile.base.api import NoAuthorizedApi
from abs.middleground.technology.permission.manager import PermissionServer


class Add(NoAuthorizedApi):
    """
    添加组织
    """
    request = with_metaclass(RequestFieldSet)
    request.appkey = RequestField(CharField, desc="appkey")
    request.organization_info = RequestField(
        DictField,
        desc="组织详情",
        conf={
            'parent_id': IntField(desc="上级组织id"),
            'name': CharField(desc="组织名称"),
            'description': CharField(desc="描述"),
            'remark': CharField(desc="备注"),
        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.organization_id = ResponseField(IntField, desc="组织Id")

    @classmethod
    def get_desc(cls):
        return "添加组织"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        organization = PermissionServer.add_organization(
            appkey=request.appkey,
            **request.organization_info
        )
        return organization

    def fill(self, response, organization):
        response.organization_id = organization.id
        return response


class All(NoAuthorizedApi):
    """
    所有组织
    """
    request = with_metaclass(RequestFieldSet)
    request.appkey = RequestField(CharField, desc="当前值")

    response = with_metaclass(ResponseFieldSet)
    response.organization_list = ResponseField(
        ListField,
        desc="组织列表",
        fmt=DictField(
            desc="组织详情",
            conf={
                "id": IntField(desc="id"),
                "name": CharField(desc="名称"),
                "remark": CharField(desc="备注"),
                "description": CharField(desc="描述"),
                "parent_id": IntField(desc="父级ID"),
                "create_time": DatetimeField(desc="创建时间"),
                'children': ListField(
                    desc="规格列表",
                    is_required=False,
                    fmt=DictField(
                        desc="组织详情",
                        conf={
                            "id": IntField(
                                desc="id",
                                is_required=False
                            ),
                            "name": CharField(
                                desc="名称",
                                is_required=False
                            ),
                            "description": CharField(
                                desc="描述",
                                is_required=False
                            ),
                            "parent_id": IntField(
                                desc="父级ID",
                                is_required=False
                            ),
                            "remark": CharField(
                                desc="备注",
                                is_required=False,
                            ),
                            "create_time": DatetimeField(
                                desc="创建时间",
                                is_required=False
                            ),
                        }
                    )
                )
            }
        )
    )

    @classmethod
    def get_desc(cls):
        return "所有组织"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        organization_list = PermissionServer.get_all_organization_byappkey(
            request.appkey
        )
        return organization_list

    def fill(self, response, organization_list):
        response.organization_list = [{
            'id': organization.id,
            'name': organization.name,
            'parent_id': organization.parent_id,
            'description': organization.description,
            'remark': organization.remark,
            'create_time': organization.create_time,
            'children': [{
                'id': sub_organization.id,
                'name': sub_organization.name,
                'parent_id': sub_organization.parent_id,
                'description': sub_organization.description,
                'remark': sub_organization.remark,
                'create_time': sub_organization.create_time,
            } for sub_organization in organization.children]
        } for organization in organization_list]
        return response


class Get(NoAuthorizedApi):
    """
    获取组织接口
    """
    request = with_metaclass(RequestFieldSet)
    request.organization_id = RequestField(IntField, desc="组织id")

    response = with_metaclass(ResponseFieldSet)
    response.organization_info = ResponseField(
        DictField,
        desc="组织详情",
        conf={
            "id": IntField(desc="名称"),
            "name": CharField(desc="名称"),
            "description": CharField(desc="描述"),
            "remark": CharField(desc="备注"),
            "parent_id": IntField(desc="父级ID"),
            "create_time": DatetimeField(desc="创建时间"),
        }
    )

    @classmethod
    def get_desc(cls):
        return "获取组织详情接口"

    @classmethod
    def get_author(cls):
        return "Roy"

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
            'create_time': organization.create_time,
        }
        return response


class Update(NoAuthorizedApi):
    """
    修改组织信息
    """
    request = with_metaclass(RequestFieldSet)
    request.organization_id = RequestField(IntField, desc="组织id")
    request.update_info = RequestField(
        DictField,
        desc="组织修改详情",
        conf={
            'name': CharField(desc="名称", is_required=False),
            'description': CharField(desc="描述", is_required=False),
            'parent_id': IntField(desc="父级ID", is_required=False),
            'remark': CharField(desc="备注", is_required=False),
        }
    )

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "修改组织信息"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        PermissionServer.update_organization(
            request.organization_id,
            **request.update_info
        )

    def fill(self, response):
        return response


class Remove(NoAuthorizedApi):
    """
    删除组织信息
    """
    request = with_metaclass(RequestFieldSet)
    request.organization_id = RequestField(IntField, desc="组织id")

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "删除组织"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        PermissionServer.remove_organization(
            request.organization_id
        )

    def fill(self, response):
        return response
