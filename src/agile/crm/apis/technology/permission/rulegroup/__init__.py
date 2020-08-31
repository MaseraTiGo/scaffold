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

from agile.crm.manager.api import StaffAuthorizedApi
from abs.middleware.config import config_middleware
from abs.middleground.technology.permission.manager import PermissionServer


class Add(StaffAuthorizedApi):
    """
    添加规则组
    """
    request = with_metaclass(RequestFieldSet)
    request.rule_group_info = RequestField(
        DictField,
        desc = "规则组详情",
        conf = {
            'name': CharField(desc = "规则组名称"),
            'content': CharField(desc = "内容, 格式参照获取全部规则"),
            'description': CharField(desc = "描述"),
            'remark': CharField(desc = "备注"),
        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.rule_group_id = ResponseField(IntField, desc = "规则组Id")

    @classmethod
    def get_desc(cls):
        return "添加规则组"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        appkey = config_middleware.get_value("common", "crm_appkey")
        rule_group = PermissionServer.add_rule_group(
            appkey = appkey,
            **request.rule_group_info
        )
        return rule_group

    def fill(self, response, rule_group):
        response.rule_group_id = rule_group.id
        return response


class Search(StaffAuthorizedApi):
    """
    所有规则组
    """
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(
        IntField,
        desc = "当前页码"
    )
    request.search_info = RequestField(
        DictField,
        desc = "搜索商品条件",
        conf = {
        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.total = ResponseField(IntField, desc = "数据总数")
    response.total_page = ResponseField(IntField, desc = "总页码数")
    response.data_list = ResponseField(
        ListField,
        desc = "规则组列表",
        fmt = DictField(
            desc = "规则组详情",
            conf = {
                'id': IntField(desc = "IDI"),
                'name': CharField(desc = "名称I"),
                'content': CharField(desc = "内容"),
                'description': CharField(desc = "描述"),
                'remark': CharField(desc = "备注"),
                'create_time': DatetimeField(desc = "创建时间"),
                'update_time': DatetimeField(desc = "更新时间"),
            }
        )
    )

    @classmethod
    def get_desc(cls):
        return "所有规则组"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        appkey = config_middleware.get_value("common", "crm_appkey")
        spliter = PermissionServer.search_rule_group(
            request.current_page,
            appkey,
            **request.search_info
        )
        return spliter

    def fill(self, response, spliter):
        response.data_list = [{
            'id': rule_group.id,
            'name': rule_group.name,
            'content': rule_group.content,
            'description': rule_group.description,
            'remark': rule_group.remark,
            'create_time': rule_group.create_time,
            'update_time': rule_group.update_time,
        } for rule_group in spliter.get_list()]
        response.total = spliter.total
        response.total_page = spliter.total_page
        return response


class Get(StaffAuthorizedApi):
    """
    获取规则组接口
    """
    request = with_metaclass(RequestFieldSet)
    request.rule_group_id = RequestField(IntField, desc = "规则组id")

    response = with_metaclass(ResponseFieldSet)
    response.rule_group_info = ResponseField(
        DictField,
        desc = "规则组详情",
        conf = {
            'id': IntField(desc = "IDI"),
            'name': CharField(desc = "名称I"),
            'content': CharField(desc = "内容"),
            'description': CharField(desc = "描述"),
            'remark': CharField(desc = "备注"),
            'create_time': DatetimeField(desc = "创建时间"),
            'update_time': DatetimeField(desc = "更新时间"),
        }
    )

    @classmethod
    def get_desc(cls):
        return "获取规则组详情接口"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        rule_group = PermissionServer.get_rule_group(
            request.rule_group_id
        )
        return rule_group

    def fill(self, response, rule_group):
        response.rule_group_info = {
            'id': rule_group.id,
            'name': rule_group.name,
            'content': rule_group.content,
            'description': rule_group.description,
            'remark': rule_group.remark,
            'create_time': rule_group.create_time,
            'update_time': rule_group.update_time,
        }
        return response


class Update(StaffAuthorizedApi):
    """
    修改规则组信息
    """
    request = with_metaclass(RequestFieldSet)
    request.rule_group_id = RequestField(IntField, desc = "规则组id")
    request.update_info = RequestField(
        DictField,
        desc = "规则组修改详情",
        conf = {
            'name': CharField(desc = "名称", is_required = False),
            'remark': CharField(desc = "备注", is_required = False),
            'content': CharField(desc = "内容", is_required = False),
            'description': CharField(desc = "描述", is_required = False),
        }
    )

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "修改规则组信息"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        PermissionServer.update_rule_group(
            request.rule_group_id,
            **request.update_info
        )

    def fill(self, response):
        return response


class Remove(StaffAuthorizedApi):
    """
    删除规则组信息
    """
    request = with_metaclass(RequestFieldSet)
    request.rule_group_id = RequestField(IntField, desc = "规则组id")

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "删除规则组"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        PermissionServer.remove_rule_group(
            request.rule_group_id
        )

    def fill(self, response):
        return response
