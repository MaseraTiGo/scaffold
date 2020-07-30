# coding=UTF-8

'''
Created on 2020年7月23日

@author: Roy
'''

from infrastructure.core.field.base import CharField, \
        IntField, ListField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet

from agile.base.api import NoAuthorizedApi
from abs.middleground.technology.permission.manager import PermissionServer


class Get(NoAuthorizedApi):
    """
    获取权限
    """
    request = with_metaclass(RequestFieldSet)
    request.appkey = RequestField(CharField, desc="授权appkey")
    request.person_id = RequestField(CharField, desc="角色Id")

    response = with_metaclass(ResponseFieldSet)
    response.operation = ResponseField(
        CharField,
        desc="操作权限"
    )
    response.data = ResponseField(
        ListField,
        desc="数据权限 - 角色列表",
        fmt=IntField(desc="角色id")
    )

    @classmethod
    def get_desc(cls):
        return "获取权限"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        permision_info = PermissionServer.get_permission(
            request.appkey,
            request.person_id,
        )
        return permision_info

    def fill(self, response, permision_info):
        response.data = permision_info.data
        response.operation = permision_info.operation
        return response
