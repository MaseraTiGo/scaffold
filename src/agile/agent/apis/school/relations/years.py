# coding=UTF-8

from infrastructure.core.field.base import CharField, DictField, \
        IntField, ListField, DatetimeField, BooleanField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet
from infrastructure.core.exception.business_error import BusinessError

from agile.crm.manager.api import StaffAuthorizedApi
from abs.services.crm.university.utils.constant import DurationTypes, \
     CategoryTypes
from abs.services.crm.university.manager import UniversityYearsServer


class All(StaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(
        ListField,
        desc = "学校专业学年列表",
        fmt = DictField(
            desc = "学校专业学年",
            conf = {
                'school_id':IntField(desc = "学校id"),
                'school_name': CharField(desc = "学校名称"),
                'children':ListField(
                    desc = "专业列表",
                    fmt = DictField(
                        desc = "专业信息",
                        conf = {
                            'major_id':IntField(desc = "专业id"),
                            'major_name': CharField(desc = "专业名称"),
                            'children':ListField(
                                desc = "学年列表",
                                fmt = DictField(
                                    desc = "专业信息",
                                    conf = {
                                        'years_id':IntField(desc = "学年id"),
                                        'category': CharField(desc = "类别"),
                                        'duration': CharField(desc = "时长"),
                                    }
                                )
                            )
                        }
                    )
                )

            }

        )
    )

    @classmethod
    def get_desc(cls):
        return "学校专业学年联动搜索接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        years_list = UniversityYearsServer.linkage()
        return years_list

    def fill(self, response, years_list):
        response.data_list = years_list
        return response
