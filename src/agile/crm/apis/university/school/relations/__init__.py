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
from abs.services.crm.university.manager import UniversityServer, \
     UniversityRelationsServer, UniversityYearsServer


class Search(StaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc = "当前页面")
    request.shcool_id = RequestField(IntField, desc = "学校id")
    request.search_info = RequestField(
        DictField,
        desc = "搜索学校专业",
        conf = {

        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.total = ResponseField(IntField, desc = "数据总数")
    response.total_page = ResponseField(IntField, desc = "总页码数")
    response.data_list = ResponseField(
        ListField,
        desc = "学校专业列表",
        fmt = DictField(
            desc = "学校专业详情",
            conf = {
                'id': IntField(desc = "id"),
                'major_id': IntField(desc = "专业id"),
                'major_name': CharField(desc = "专业名称"),
                'create_time': DatetimeField(desc = "创建时间"),
                'years_list':ListField(
                    desc = "学年列表",
                    fmt = DictField(
                        desc = "工作流信息",
                        conf = {
                            'category':CharField(
                                 desc = "分类",
                                 choices = CategoryTypes.CHOICES
                             ),
                             'duration':CharField(
                                 desc = "时长",
                                 choices = DurationTypes.CHOICES
                             ),
                        }
                    )
                )
            }
        )
    )

    @classmethod
    def get_desc(cls):
        return "学校专业搜索接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        school = UniversityServer.get_school(request.shcool_id)
        request.search_info.update({"school":school})
        spliter = UniversityRelationsServer.search(
            request.current_page,
            **request.search_info
        )
        UniversityYearsServer.hung_years_byrelations(spliter.data)
        return spliter

    def fill(self, response, spliter):
        data_list = [{
                        "id":relations.id,
                        "major_id":relations.major.id,
                        "major_name":relations.major.name,
                        "create_time":relations.create_time,
                        "years_list":[{
                            "category":years.category,
                            "duration":years.duration,
                        } for years in relations.years_list]
                      } for relations in spliter.data]
        response.data_list = data_list
        response.total = spliter.total
        response.total_page = spliter.total_page
        return response


class Add(StaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.shcool_id = RequestField(IntField, desc = "学校id")
    request.relations_info = RequestField(
        DictField,
        desc = "学校专业信息",
        conf = {
                'major_id': IntField(desc = "专业id"),
                'years_list':ListField(
                    desc = "学年列表",
                    fmt = DictField(
                        desc = "工作流信息",
                        conf = {
                            'category':CharField(
                                 desc = "分类",
                                 choices = CategoryTypes.CHOICES
                             ),
                             'duration':CharField(
                                 desc = "时长",
                                 choices = DurationTypes.CHOICES
                             ),
                        }
                    )
                )

        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.relations_id = ResponseField(IntField, desc = "id")

    @classmethod
    def get_desc(cls):
        return "学校专业创建接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        school = UniversityServer.get_school(request.shcool_id)
        major_id = request.relations_info.pop("major_id")
        years_list = request.relations_info.pop("years_list")
        major = UniversityServer.get_major(major_id)
        request.relations_info.update({
            "school":school,
            "major":major
        })
        relations = UniversityRelationsServer.create(
            **request.relations_info
        )
        UniversityYearsServer.batch_create(
            years_list,
            relations
        )
        return relations

    def fill(self, response, relations):
        response.relations_id = relations.id
        return response


class Update(StaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.relations_id = RequestField(IntField, desc = "学校专业id")
    request.relations_info = RequestField(
        DictField,
        desc = "需要更新的学校专业信息",
        conf = {
                'major_id': IntField(desc = "专业id"),
        }
    )
    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "学校专业更新接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        major_id = request.relations_info.pop("major_id")
        major = UniversityServer.get_major(major_id)
        request.relations_info.update({
            "major":major
        })
        relations = UniversityRelationsServer.update(
            request.relations_id,
            **request.relations_info
        )

    def fill(self, response):
        return response


class Remove(StaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.relations_id = RequestField(IntField, desc = "学校专业id")

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "学校专业删除接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        UniversityRelationsServer.remove(
            request.relations_id
        )

    def fill(self, response):
        return response
