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
        UseStatus, PermissionTypes


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
        company = EnterpriseServer.get(
            request.authorize_info.company_id
        )
        authorization = PermissionServer.authorize(
            request.platform_id,
            company_name=company.name,
            **request.authorize_info
        )
        return authorization

    def fill(self, response, authorization):
        response.appkey = authorization.appkey
        return response


class Apply(StaffAuthorizedApi):
    """
    使用授权
    """
    request = with_metaclass(RequestFieldSet)
    request.appkey = RequestField(CharField, desc="授权appkey")

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        authorization = PermissionServer.apply(request.appkey)
        return authorization

    def fill(self, response, authorization):
        return response


class Forbidden(StaffAuthorizedApi):
    """
    禁用授权
    """
    request = with_metaclass(RequestFieldSet)
    request.appkey = RequestField(CharField, desc="授权appkey")

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        authorization = PermissionServer.forbidden(request.appkey)
        return authorization

    def fill(self, response, authorization):
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
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        authorization = PermissionServer.refresh(request.appkey)
        return authorization

    def fill(self, response, authorization):
        response.appkey = authorization.appkey
        return response


class Search(StaffAuthorizedApi):
    """
    获取所有授权列表
    """
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(
        IntField,
        desc="当前页码"
    )
    request.platform_id = RequestField(
        IntField,
        desc="平台id"
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
        desc="授权列表",
        fmt=DictField(
            desc="授权详情",
            conf={
                'id': IntField(desc="授权id"),
                'appkey': CharField(desc="appkey"),
                'use_status': CharField(
                    desc="use_status",
                    choices=UseStatus.CHOICES,
                ),
                'company_id': IntField(desc="公司ID"),
                'company_name': CharField(desc="公司"),
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
        spliter = PermissionServer.search_authorization(
            request.current_page,
            request.platform_id,
            **request.search_info,
        )
        return spliter

    def fill(self, response, spliter):
        response.data_list = [
            {
                'id': authorization.id,
                'appkey': authorization.appkey,
                'use_status': authorization.use_status,
                'company_id': authorization.company_id,
                'company_name': authorization.company_name,
                'remark': authorization.remark,
                'create_time': authorization.create_time,
                'update_time': authorization.update_time,
            }
            for authorization in spliter.get_list()
        ]
        response.total = spliter.total
        response.total_page = spliter.total_page
        return response


class Get(StaffAuthorizedApi):
    """
    获取授权详情
    """
    request = with_metaclass(RequestFieldSet)
    request.authorization_id = RequestField(IntField, desc="授权id")

    response = with_metaclass(ResponseFieldSet)
    response.authorization_info = ResponseField(
        DictField,
        desc="授权详情",
        conf={
            'id': IntField(desc="授权id"),
            'appkey': CharField(desc="appkey"),
            'use_status': CharField(
                desc="use_status",
                choices=UseStatus.CHOICES,
            ),
            'company_id': IntField(desc="公司ID"),
            'company_name': CharField(desc="公司"),
            'remark': CharField(desc="备注"),
            'update_time': CharField(desc="修改时间"),
            'create_time': CharField(desc="创建时间"),
        }
    )

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        spliter = PermissionServer.get_authorization(
            request.authorization_id,
        )
        return spliter

    def fill(self, response, authorization):
        response.authorization_info = {
            'id': authorization.id,
            'appkey': authorization.appkey,
            'use_status': authorization.use_status,
            'company_id': authorization.company_id,
            'company_name': authorization.company_name,
            'remark': authorization.remark,
            'create_time': authorization.create_time,
            'update_time': authorization.update_time,
        }
        return response


class Update(StaffAuthorizedApi):
    """
    更新授权信息
    """
    request = with_metaclass(RequestFieldSet)
    request.authorization_id = RequestField(IntField, desc="授权id")
    request.update_info = RequestField(
        DictField,
        desc="更新内容",
        conf={
            'remark': CharField(desc="备注", is_required=False),
            'use_status': CharField(
                desc="use_status",
                choices=UseStatus.CHOICES,
                is_required=False,
            ),
        }
    )

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        PermissionServer.update_authorization(
            request.authorization_id,
            **request.update_info
        )

    def fill(self, response):
        return response


class Remove(StaffAuthorizedApi):
    """
    删除授权信息
    """
    request = with_metaclass(RequestFieldSet)
    request.authorization_id = RequestField(IntField, desc="平台id")

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        PermissionServer.remove_authorization(
            request.authorization_id,
        )

    def fill(self, response):
        return response
