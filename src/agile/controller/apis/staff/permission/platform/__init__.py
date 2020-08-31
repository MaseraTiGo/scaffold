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
from abs.middleground.business.enterprise.manager import EnterpriseServer
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
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        company = EnterpriseServer.get(request.authorize_info.company_id)
        platform = PermissionServer.create_platform(
            company_name=company.name,
            **request.authorize_info
        )
        return platform

    def fill(self, response, platform):
        response.platform_id = platform.id
        return response


class Search(StaffAuthorizedApi):
    """
    获取所有平台列表
    """
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(
        IntField,
        desc="当前页码"
    )
    request.search_info = RequestField(
        DictField,
        desc="搜索条件",
        conf={
            'name': CharField(desc="平台名称", is_required=False),
        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.total = ResponseField(IntField, desc="数据总数")
    response.total_page = ResponseField(IntField, desc="总页码数")
    response.data_list = ResponseField(
        ListField,
        desc="平台列表",
        fmt=DictField(
            desc="平台详情",
            conf={
                'id': IntField(desc="平台id"),
                'name': CharField(desc="平台名称"),
                'app_type': CharField(
                    desc="平台类型",
                    choices=PermissionTypes.CHOICES
                ),
                'company_id': IntField(desc="公司ID"),
                'company_name': CharField(desc="公司ID"),
                'remark': CharField(desc="备注"),
                'update_time': CharField(desc="修改时间"),
                'create_time': CharField(desc="创建时间"),
            }
        )
    )

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        spliter = PermissionServer.search_platform(
            request.current_page,
            **request.search_info,
        )
        return spliter

    def fill(self, response, spliter):
        response.data_list = [
            {
                'id': platform.id,
                'name': platform.name,
                'company_id': platform.company_id,
                'company_name': platform.company_name,
                'app_type': platform.app_type,
                'remark': platform.remark,
                'create_time': platform.create_time,
                'update_time': platform.update_time,
            }
            for platform in spliter.get_list()
        ]
        response.total = spliter.total
        response.total_page = spliter.total_page
        return response


class Get(StaffAuthorizedApi):
    """
    获取平台详情
    """
    request = with_metaclass(RequestFieldSet)
    request.platform_id = RequestField(IntField, desc="平台id")

    response = with_metaclass(ResponseFieldSet)
    response.platform_info = ResponseField(
        DictField,
        desc="平台详情",
        conf={
            'id': IntField(desc="平台id"),
            'name': CharField(desc="平台名称"),
            'app_type': CharField(
                desc="平台类型",
                choices=PermissionTypes.CHOICES
            ),
            'company_id': IntField(desc="公司ID"),
            'company_name': CharField(desc="公司ID"),
            'remark': CharField(desc="备注"),
            'update_time': CharField(desc="修改时间"),
            'create_time': CharField(desc="创建时间"),
        }
    )

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        spliter = PermissionServer.get_platform(
            request.platform_id,
        )
        return spliter

    def fill(self, response, platform):
        response.platform_info = {
            'id': platform.id,
            'name': platform.name,
            'company_id': platform.company_id,
            'company_name': platform.company_name,
            'app_type': platform.app_type,
            'remark': platform.remark,
            'create_time': platform.create_time,
            'update_time': platform.update_time,
        }
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
            'name': CharField(desc="平台名称", is_required=False),
            'company_id': IntField(desc="公司ID", is_required=False),
            'app_type': CharField(
                desc="平台类型",
                is_required=False,
                choices=PermissionTypes.CHOICES
            ),
            'remark': CharField(desc="备注", is_required=False),
        }
    )

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        if 'company_id' in request.update_info:
            company = EnterpriseServer.get(
                request.update_info.company_id
            )
            request.update_info.update({
                'company_name': company.name
            })
        PermissionServer.update_platform(
            request.platform_id,
            **request.update_info
        )

    def fill(self, response):
        return response


class Remove(StaffAuthorizedApi):
    """
    删除平台信息
    """
    request = with_metaclass(RequestFieldSet)
    request.platform_id = RequestField(IntField, desc="平台id")

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        PermissionServer.remove_platform(
            request.platform_id,
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
