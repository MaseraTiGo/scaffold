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

from agile.controller.manager.api import StaffAuthorizedApi
from abs.services.controller.staff.manager import StaffServer
from abs.middleground.technology.permission.manager import PermissionServer


class Add(StaffAuthorizedApi):
    """
    添加组织
    """
    request = with_metaclass(RequestFieldSet)
    request.organization_info = RequestField(
        DictField,
        desc="组织详情",
        conf={
            'parent_id': IntField(desc="上级组织id"),
            'position_id_list': ListField(
                desc="组织id列表",
                fmt=IntField(desc="组织id")
            ),
            'name': CharField(desc="组织名称"),
            'description': CharField(desc="描述"),
            'remark': CharField(desc="备注"),
        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.organization_id = ResponseField(IntField, desc="组织Id")

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        staff_id = self.auth_user.id
        staff = StaffServer.get(staff_id)
        organization = PermissionServer.add_organization(
            appkey=staff.company.permission_key,
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
                "position_list": ListField(
                    desc="职位列表",
                    fmt=DictField(
                        desc="身份详情",
                        conf={
                            'id': IntField(desc="职位id"),
                            'name': CharField(desc="职位名称"),
                        }
                    )
                ),
            }
        )
    )

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        staff_id = self.auth_user.id
        staff = StaffServer.get(staff_id)
        organization_list = PermissionServer.get_all_organization_byappkey(
            staff.company.permission_key,
        )
        return organization_list

    def fill(self, response, organization_list):
        response.organization_list = [
            {
                'id': organization.id,
                'name': organization.name,
                'remark': organization.remark,
                'description': organization.description,
                'parent_id': organization.parent_id,
                'position_list': [
                    {
                        "id": position['id'],
                        "name": position['name'],
                    }
                    for position in organization.position_list
                ],
            }
            for organization in organization_list
        ]
        return response


class Tree(StaffAuthorizedApi):
    """
    树状组织结构图
    """
    request = with_metaclass(RequestFieldSet)

    response = with_metaclass(ResponseFieldSet)
    response.organization_list = ResponseField(
        ListField,
        desc="组织列表",
        fmt=IterationField(
            desc="组织详情",
            flag="children",
            fmt={
                "id": IntField(desc="id"),
                "name": CharField(desc="名称"),
                "remark": CharField(desc="备注"),
                "description": CharField(desc="描述"),
                "parent_id": IntField(desc="父级ID"),
                "update_time": DatetimeField(desc="更新时间"),
                "create_time": DatetimeField(desc="创建时间"),
                "position_list": ListField(
                    desc="职位列表",
                    fmt=DictField(
                        desc="身份详情",
                        conf={
                            'id': IntField(desc="职位id"),
                            'name': CharField(desc="职位名称"),
                        }
                    )
                ),
            }
        )
    )

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        staff_id = self.auth_user.id
        staff = StaffServer.get(staff_id)
        organization_list = PermissionServer.get_tree_organization_byappkey(
            staff.company.permission_key,
        )
        return organization_list

    def fill(self, response, organization_list):
        response.organization_list = organization_list
        return response


class Search(StaffAuthorizedApi):
    """
    搜索组织
    """
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(
        IntField,
        desc="当前页码"
    )
    request.search_info = RequestField(
        DictField,
        desc="搜索规则组",
        conf={
            'name': CharField(desc="名称", is_required=False),
        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.total = ResponseField(IntField, desc="数据总数")
    response.total_page = ResponseField(IntField, desc="总页码数")
    response.data_list = ResponseField(
        ListField,
        desc="组织列表",
        fmt=DictField(
            desc="组织详情",
            conf={
                "id": IntField(desc="ID"),
                "name": CharField(desc="名称"),
                "position_list": ListField(
                    desc="职位列表",
                    fmt=DictField(
                        desc="身份详情",
                        conf={
                            'id': IntField(desc="职位id"),
                            'name': CharField(desc="职位名称"),
                        }
                    )
                ),
                "description": CharField(desc="描述"),
                "remark": CharField(desc="备注"),
            }
        )
    )

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        staff_id = self.auth_user.id
        staff = StaffServer.get(staff_id)
        spliter = PermissionServer.search_organization_byappkey(
            staff.company.permission_key,
            request.current_page,
            **request.search_info,
        )
        return spliter

    def fill(self, response, spliter):
        response.data_list = [{
            'id': organization.id,
            'name': organization.name,
            'position_list': [
                {
                    "id": position.id,
                    "name": position.name,
                }
                for position in organization.position_list
            ],
            'description': organization.description,
            'remark': organization.remark,
        } for organization in spliter.get_list()]
        response.total = spliter.total
        response.total_page = spliter.total_page
        return response


class Get(StaffAuthorizedApi):
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
            "position_id_list": CharField(desc="身份列表"),
            "position_list": ListField(
                desc="职位列表",
                fmt=DictField(
                    desc="身份详情",
                    conf={
                        'id': IntField(desc="职位id"),
                        'name': CharField(desc="职位名称"),
                    }
                )
            ),
            "remark": CharField(desc="备注"),
            "parent_id": IntField(desc="父级ID"),
            "create_time": DatetimeField(desc="创建时间"),
            "update_time": DatetimeField(desc="更新时间"),
        }
    )

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
            'position_id_list': organization.position_id_list,
            'position_list': [
                {
                    "id": position.id,
                    "name": position.name,
                }
                for position in organization.position_list
            ],
            'description': organization.description,
            'remark': organization.remark,
            'create_time': organization.create_time,
            'update_time': organization.update_time,
        }
        return response


class Update(StaffAuthorizedApi):
    """
    修改组织信息
    """
    request = with_metaclass(RequestFieldSet)
    request.organization_id = RequestField(IntField, desc="组织id")
    request.update_info = RequestField(
        DictField,
        desc="组织修改详情",
        conf={
            'position_id_list': ListField(
                desc="职位id列表",
                fmt=IntField(desc="职位id")
            ),
            'name': CharField(desc="名称", is_required=False),
            'description': CharField(desc="描述", is_required=False),
            'parent_id': IntField(desc="父级ID", is_required=False),
            'remark': CharField(desc="备注", is_required=False),
        }
    )

    response = with_metaclass(ResponseFieldSet)

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


class Remove(StaffAuthorizedApi):
    """
    删除组织信息
    """
    request = with_metaclass(RequestFieldSet)
    request.organization_id = RequestField(IntField, desc="组织id")

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        PermissionServer.remove_organization(
            request.organization_id
        )

    def fill(self, response):
        return response
