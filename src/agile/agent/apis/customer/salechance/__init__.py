# coding=UTF-8

from infrastructure.core.field.base import CharField, DictField, \
        IntField, ListField, DatetimeField, BooleanField, DateField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet
from infrastructure.core.exception.business_error import BusinessError

from agile.agent.manager.api import AgentStaffAuthorizedApi
from abs.services.crm.university.manager import UniversityServer


class Search(AgentStaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(
        ListField,
        desc = "机会列表",
        fmt = DictField(
            desc = "机会列表",
            conf = {
                'id': IntField(desc = "机会id"),
                'phone': CharField(desc = "专业名称"),
                'name': CharField(desc = "专业名称"),
                'wechat': CharField(desc = "专业名称"),
                'education': CharField(desc = "专业名称"),
                'production_id': IntField(desc = "专业名称"),
                'production_name': CharField(desc = "专业名称"),
                'city': CharField(desc = "专业名称"),
                'name': CharField(desc = "专业名称"),
                'staff_id': IntField(desc = "专业名称"),
                'staff_name': CharField(desc = "专业名称"),
                'end_time': DateField(desc = "专业名称"),
                'create_time': DatetimeField(desc = "专业名称"),
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







