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
        desc = "学校列表",
        fmt = DictField(
            desc = "学校内容",
            conf = {
                'id': IntField(desc = "学校id"),
                'name': CharField(desc = "学校名称"),
            }
        )
    )

    @classmethod
    def get_desc(cls):
        return "学校搜索全部接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        school_list = UniversityServer.search_all_school()
        return school_list

    def fill(self, response, school_list):
        data_list = [{
                "id":school.id,
                "name":school.name,
              }  for school in school_list]
        response.data_list = data_list
        return response

