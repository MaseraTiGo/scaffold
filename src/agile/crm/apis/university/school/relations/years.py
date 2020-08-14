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
from abs.services.agent.goods.manager import GoodsServer


class Search(StaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.relations_id = RequestField(IntField, desc = "学校专业id")
    request.search_info = RequestField(
        DictField,
        desc = "搜索学校专业",
        conf = {

        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(
        ListField,
        desc = "学校专业列表",
        fmt = DictField(
            desc = "学校专业详情",
            conf = {
                'id': IntField(desc = "id"),
                'category': CharField(desc = "类别"),
                'duration': CharField(desc = "市场"),
                'create_time': DatetimeField(desc = "创建时间"),
            }
        )
    )

    @classmethod
    def get_desc(cls):
        return "学年搜索接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        relations = UniversityRelationsServer.get(request.relations_id)
        request.search_info.update({"relations":relations})
        years_list = UniversityYearsServer.search_all(
            **request.search_info
        )
        return years_list

    def fill(self, response, years_list):
        data_list = [{
                        "id":years.id,
                        "category":years.category,
                        "duration":years.duration,
                        "create_time":years.create_time,
                      } for years in years_list]
        response.data_list = data_list
        return response


class Add(StaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.relations_id = RequestField(IntField, desc = "学校id")
    request.years_info = RequestField(
        DictField,
        desc = "学年信息",
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

    response = with_metaclass(ResponseFieldSet)
    response.years_id = ResponseField(IntField, desc = "id")

    @classmethod
    def get_desc(cls):
        return "学年创建接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        relations = UniversityRelationsServer.get(request.relations_id)
        request.years_info.update({
            "relations":relations,
        })
        years = UniversityYearsServer.create(
            **request.years_info
        )
        return years

    def fill(self, response, years):
        response.years_id = years.id
        return response


class Update(StaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.years_id = RequestField(IntField, desc = "学年id")
    request.years_info = RequestField(
        DictField,
        desc = "需要更新得学年信息",
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
    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "学年更新接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        years = UniversityYearsServer.update(
            request.years_id,
            **request.years_info
        )

    def fill(self, response):
        return response


class Remove(StaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.years_id = RequestField(IntField, desc = "学年id")

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "学年删除接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        goods_qs = GoodsServer.search_all_goods(
            years_id = request.years_id
        )
        if goods_qs.count() > 0:
            raise BusinessError("专业已绑定商品禁止删除")
        UniversityYearsServer.remove(
            request.years_id
        )

    def fill(self, response):
        return response