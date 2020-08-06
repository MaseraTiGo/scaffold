# coding=UTF-8

from infrastructure.core.field.base import CharField, DictField, \
        IntField, ListField, DatetimeField, BooleanField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet
from infrastructure.core.exception.business_error import BusinessError

from agile.agent.manager.api import AgentStaffAuthorizedApi
from abs.services.crm.university.manager import UniversityServer



class SearchAll(AgentStaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(
        ListField,
        desc = "专业列表",
        fmt = DictField(
            desc = "专业内容",
            conf = {
                'id': IntField(desc = "专业id"),
                'name': CharField(desc = "专业名称"),
            }
        )
    )

    @classmethod
    def get_desc(cls):
        return "专业搜索"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        major_list = UniversityServer.search_all_major()
        return major_list

    def fill(self, response, major_list):
        data_list = [{
            "id":major.id,
            "name":major.name,
          }  for major in major_list]
        response.data_list = data_list
        return response







