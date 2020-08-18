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
    添加规则
    """
    request = with_metaclass(RequestFieldSet)
    request.platform_id = RequestField(IntField, desc="平台id")
    request.rule_info = RequestField(
        DictField,
        desc="规则详情",
        conf={
            'name': CharField(desc="规则名称"),
            'parent_id': IntField(desc="上级规则id"),
            'description': CharField(desc="描述"),
            'remark': CharField(desc="备注"),
        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.rule_id = ResponseField(IntField, desc="规则Id")

    @classmethod
    def get_desc(cls):
        return "添加规则"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        rule = PermissionServer.add_rule(
            platform_id=request.platform_id,
            **request.rule_info
        )
        return rule

    def fill(self, response, rule):
        response.rule_id = rule.id
        return response


class All(NoAuthorizedApi):
    """
    所有规则
    """
    request = with_metaclass(RequestFieldSet)
    request.platform_id = RequestField(IntField, desc="平台id")

    response = with_metaclass(ResponseFieldSet)
    response.rule_list = ResponseField(
        ListField,
        desc="规则列表",
        fmt=DictField(
            desc="规则详情",
            conf={
                'name': CharField(desc="名称I"),
                'code': CharField(desc="编码"),
                'children': ListField(
                    desc="规格列表",
                    is_required=False,
                    fmt=DictField(
                        desc="规则详情",
                        conf={
                            "name": CharField(desc="名称"),
                            "code": CharField(desc="展示图片"),
                        }
                    )
                )
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
        rule_list = PermissionServer.get_all_rule_byplatform(
            request.platform_id
        )
        return rule_list

    def fill(self, response, rule_list):
        response.rule_list = [{
            'name': rule.name,
            'code': rule.code,
            'children': [{
                'name': sub_rule.name,
                'code': sub_rule.code,
            } for sub_rule in rule.children]
        } for rule in rule_list]
        return response


class Get(NoAuthorizedApi):
    """
    获取规则接口
    """
    request = with_metaclass(RequestFieldSet)
    request.rule_id = RequestField(IntField, desc="规则id")

    response = with_metaclass(ResponseFieldSet)
    response.rule_info = ResponseField(
        DictField,
        desc="规则详情",
        conf={
            'id': IntField(desc="ID"),
            'name': CharField(desc="名称"),
            'code': CharField(desc="编码"),
            'parent_id': IntField(desc="父级ID"),
            'remark': CharField(desc="备注"),
            'create_time': DatetimeField(desc="创建时间"),
        }
    )

    @classmethod
    def get_desc(cls):
        return "获取规则详情接口"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        rule = PermissionServer.get_rule(request.rule_id)
        return rule

    def fill(self, response, rule):
        response.rule_info = {
            'id': rule.id,
            'name': rule.name,
            'code': rule.code,
            'remark': rule.remark,
            'parent_id': rule.parent_id,
            'create_time': rule.create_time,
        }
        return response


class Update(NoAuthorizedApi):
    """
    修改规则信息
    """
    request = with_metaclass(RequestFieldSet)
    request.rule_id = RequestField(IntField, desc="规则id")
    request.update_info = RequestField(
        DictField,
        desc="规则修改详情",
        conf={
            'name': CharField(desc="名称", is_required=False),
            'parent_id': IntField(desc="父级ID", is_required=False),
            'remark': CharField(desc="备注", is_required=False),
        }
    )

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "修改规则信息"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        PermissionServer.update_rule(
            request.rule_id,
            **request.update_info
        )

    def fill(self, response):
        return response


class Remove(NoAuthorizedApi):
    """
    删除规则信息
    """
    request = with_metaclass(RequestFieldSet)
    request.rule_id = RequestField(IntField, desc="规则id")

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "删除规则"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        PermissionServer.remove_rule(
            request.rule_id
        )

    def fill(self, response):
        return response
