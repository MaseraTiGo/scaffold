# coding=UTF-8

from infrastructure.core.field.base import CharField, DictField, \
        IntField, ListField, BooleanField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet

from agile.customer.manager.api import CustomerAuthorizedApi


class All(CustomerAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.search_info = RequestField(
        DictField,
        desc="搜索专业",
        conf={
        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(
        ListField,
        desc="专业列表",
        fmt=DictField(
            desc="专业信息",
            conf={
                'id': IntField(desc="学校id"),
                'name': CharField(desc="名称")
            }
        )
    )

    @classmethod
    def get_desc(cls):
        return "专业列表"

    @classmethod
    def get_author(cls):
        return "xyc"

    def execute(self, request):
        major_list = []
        return major_list

    def fill(self, response, major_list):
        data_list = []
        response.data_list = data_list
        return response
