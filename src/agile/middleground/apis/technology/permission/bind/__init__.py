# coding=UTF-8

'''
Created on 2020年7月23日

@author: Roy
'''

from infrastructure.core.field.base import CharField, DictField, \
        IntField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseFieldSet

from agile.base.api import NoAuthorizedApi
from abs.middleground.technology.permission.manager import PermissionServer


class Position(NoAuthorizedApi):
    """
    绑定身份
    """
    request = with_metaclass(RequestFieldSet)
    request.appkey = RequestField(CharField, desc="appkey")
    request.bind_info = RequestField(
        DictField,
        desc="绑定信息",
        conf={
            'organization_id': IntField(desc="组织id"),
            'position_id': IntField(desc="身份ID"),
            'person_id': IntField(desc="角色ID"),
        }
    )

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "绑定身份"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        rule = PermissionServer.bind_position(
            request.appkey,
            **request.bind_info
        )
        return rule

    def fill(self, response, rule):
        return response


class Person(NoAuthorizedApi):
    """
    绑定个人
    """
    request = with_metaclass(RequestFieldSet)
    request.appkey = RequestField(CharField, desc="appkey")
    request.bind_info = RequestField(
        DictField,
        desc="绑定信息",
        conf={
            'person_group_id': IntField(desc="用户组id"),
            'person_id': IntField(desc="角色ID"),
        }
    )

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "绑定个人"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        rule = PermissionServer.bind_person(
            request.appkey,
            **request.bind_info
        )
        return rule

    def fill(self, response, rule):
        return response
