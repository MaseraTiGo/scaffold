# coding=UTF-8

from infrastructure.core.field.base import CharField, DictField, \
        IntField, ListField, BooleanField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet

from agile.customer.manager.api import CustomerAuthorizedApi
from abs.services.crm.university.manager import UniversityServer


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
        major_list = UniversityServer.search_all_major(**request.search_info)
        return major_list

    def fill(self, response, major_list):
        data_list = [{
            'id': major.id,
            'name': major.name
        } for major in major_list]
        response.data_list = data_list
        return response


class Duration(CustomerAuthorizedApi):
    request = with_metaclass(RequestFieldSet)

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(
        ListField,
        desc="学年列表",
        fmt=DictField(
            desc="专业信息",
            conf={
                'id': CharField(desc="key"),
                'name': CharField(desc="值")
            }
        )
    )

    @classmethod
    def get_desc(cls):
        return "学年列表"

    @classmethod
    def get_author(cls):
        return "xyc"

    def execute(self, request):
        duration_mapping = UniversityServer.get_duration()
        return duration_mapping

    def fill(self, response, duration_mapping):
        data_list = [{
            'id': key,
            'name': value
        } for key, value in duration_mapping.items()]
        response.data_list = data_list
        return response
