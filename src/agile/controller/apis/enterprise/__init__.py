# coding=UTF-8

'''
Created on 2016年7月23日

@author: Administrator
'''

from infrastructure.core.field.base import CharField, DictField, \
        IntField, ListField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet

from agile.controller.manager.api import StaffAuthorizedApi
from abs.middleground.business.enterprise.manager import EnterpriseServer


class Search(StaffAuthorizedApi):
    """
    搜索公司
    """
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(
        IntField,
        desc="当前页码"
    )
    request.search_info = RequestField(
        DictField,
        desc="搜索公司条件",
        conf={
            'name': CharField(desc="公司名称", is_required=False),
        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.total = ResponseField(IntField, desc="数据总数")
    response.total_page = ResponseField(IntField, desc="总页码数")
    response.data_list = ResponseField(
        ListField,
        desc="公司列表",
        fmt=DictField(
            desc="公司详情",
            conf={
                'id': IntField(desc="编号"),
                'name': CharField(desc="公司名称"),
            }
        )
    )
    response.total = ResponseField(IntField, desc="数据总数")
    response.total_page = ResponseField(IntField, desc="总页码数")

    @classmethod
    def get_desc(cls):
        return "搜索公司"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        enterprise_spliter = EnterpriseServer.search(
            request.current_page,
            **request.search_info
        )
        return enterprise_spliter

    def fill(self, response, enterprise_spliter):
        data_list = [{
            'id': enterprise.id,
            'name': enterprise.name,
        } for enterprise in enterprise_spliter.data]
        response.data_list = data_list
        response.total = enterprise_spliter.total
        response.total_page = enterprise_spliter.total_page
        return response
