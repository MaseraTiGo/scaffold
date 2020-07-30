# coding=UTF-8

'''
Created on 2020年7月23日

@author: Roy
'''

from infrastructure.core.field.base import CharField, DictField, \
        IntField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet

from agile.base.api import NoAuthorizedApi
from abs.middleground.technology.permission.manager import PermissionServer
from abs.middleground.technology.permission.utils.constant import \
        PermissionTypes


class Authorize(NoAuthorizedApi):
    """
    添加授权
    """
    request = with_metaclass(RequestFieldSet)
    request.authorize_info = RequestField(
        DictField,
        desc="授权详情",
        conf={
            'name': CharField(desc="平台名称"),
            'company_id': IntField(desc="公司ID"),
            'app_type': CharField(
                desc="授权类型",
                choices=PermissionTypes.CHOICES,
            ),
            'prefix': CharField(desc="前缀，仅允许2位"),
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
            **request.authorize_info
        )
        return platform

    def fill(self, response, platform):
        response.appkey = platform.appkey
        return response


class Apply(NoAuthorizedApi):
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


class Forbidden(NoAuthorizedApi):
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


class Refresh(NoAuthorizedApi):
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
