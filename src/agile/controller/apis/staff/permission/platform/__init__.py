# coding=UTF-8

'''
Created on 2020年7月23日

@author: Roy
'''

from infrastructure.core.field.base import CharField, DictField, \
        IntField, ListField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet

from agile.controller.manager.api import StaffAuthorizedApi
from abs.middleground.technology.permission.manager import PermissionServer
from abs.middleground.technology.permission.utils.constant import \
        PermissionTypes


class Add(StaffAuthorizedApi):
    """
    添加平台
    """
    request = with_metaclass(RequestFieldSet)
    request.authorize_info = RequestField(
        DictField,
        desc="授权详情",
        conf={
            'name': CharField(desc="平台名称"),
            'company_id': IntField(desc="公司ID"),
            'app_type': CharField(
                desc="平台类型",
                choices=PermissionTypes.CHOICES
            ),
            'remark': CharField(desc="备注"),
        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.platform_id = ResponseField(IntField, desc="平台id")

    @classmethod
    def get_desc(cls):
        return "添加授权"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        platform = PermissionServer.create_platform(
            **request.authorize_info
        )
        return platform

    def fill(self, response, platform):
        response.platform_id = platform.id
        return response


class All(StaffAuthorizedApi):
    """
    获取所有平台列表
    """
    request = with_metaclass(RequestFieldSet)

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(
        ListField,
        desc="平台列表",
        fmt=DictField(
            desc="平台详情",
            conf={
                'id': IntField(desc="平台id"),
                'name': CharField(desc="平台名称"),
                'company_id': IntField(desc="公司ID"),
                'remark': CharField(desc="备注"),
            }
        )
    )

    @classmethod
    def get_desc(cls):
        return "获取所有平台列表"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        platform_list = PermissionServer.all_platform()
        return platform_list

    def fill(self, response, platform_list):
        response.data_list = [
            {
                'id': platform.id,
                'name': platform.name,
                'company_id': platform.company_id,
                'remark': platform.remark,
            }
            for platform in platform_list
        ]
        return response


class Update(StaffAuthorizedApi):
    """
    更新平台信息
    """
    request = with_metaclass(RequestFieldSet)
    request.platform_id = RequestField(IntField, desc="平台id")
    request.update_info = RequestField(
        DictField,
        desc="更新内容",
        conf={
            'name': CharField(desc="平台名称"),
            'remark': CharField(desc="备注"),
        }
    )

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "更新平台信息"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        PermissionServer.update_platform(
            request.platform_id,
            **request.update_info
        )

    def fill(self, response):
        return response


class Authorize(StaffAuthorizedApi):
    """
    添加授权
    """
    request = with_metaclass(RequestFieldSet)
    request.platform_id = RequestField(IntField, desc="平台id")
    request.authorize_info = RequestField(
        DictField,
        desc="授权详情",
        conf={
            'company_id': IntField(desc="公司ID"),
            'remark': CharField(desc="备注"),
        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.appkey = ResponseField(CharField, desc="访问appkey")

    @classmethod
    def get_desc(cls):
        return "添加授权"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        platform = PermissionServer.authorize(
            request.platform_id,
            **request.authorize_info
        )
        return platform

    def fill(self, response, platform):
        response.appkey = platform.appkey
        return response


class Apply(StaffAuthorizedApi):
    """
    使用授权
    """
    request = with_metaclass(RequestFieldSet)
    request.appkey = RequestField(CharField, desc="授权appkey")

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "使用授权"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        platform = PermissionServer.apply(request.appkey)
        return platform

    def fill(self, response, platform):
        return response


class Forbidden(StaffAuthorizedApi):
    """
    禁用授权
    """
    request = with_metaclass(RequestFieldSet)
    request.appkey = RequestField(CharField, desc="授权appkey")

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "禁用授权"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        platform = PermissionServer.forbidden(request.appkey)
        return platform

    def fill(self, response, platform):
        return response


class Refresh(StaffAuthorizedApi):
    """
    刷新授权
    """
    request = with_metaclass(RequestFieldSet)
    request.appkey = RequestField(CharField, desc="授权appkey")

    response = with_metaclass(ResponseFieldSet)
    response.appkey = ResponseField(CharField, desc="新授权appkey")

    @classmethod
    def get_desc(cls):
        return "刷新授权"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        platform = PermissionServer.refresh(request.appkey)
        return platform

    def fill(self, response, platform):
        response.appkey = platform.appkey
        return response
