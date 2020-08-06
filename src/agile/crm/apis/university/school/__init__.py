# coding=UTF-8

from infrastructure.core.field.base import CharField, DictField, \
        IntField, ListField, DatetimeField, BooleanField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet
from infrastructure.core.exception.business_error import BusinessError

from agile.crm.manager.api import StaffAuthorizedApi
from abs.services.crm.university.manager import UniversityServer
from abs.services.agent.goods.manager import GoodsServer


class Search(StaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc = "当前页面")
    request.search_info = RequestField(
        DictField,
        desc = "搜索学校",
        conf = {
              'name': CharField(desc = "学校名称", is_required = False),
        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.total = ResponseField(IntField, desc = "数据总数")
    response.total_page = ResponseField(IntField, desc = "总页码数")
    response.data_list = ResponseField(
        ListField,
        desc = "学校列表",
        fmt = DictField(
            desc = "学校内容",
            conf = {
                'id': IntField(desc = "学校id"),
                'name': CharField(desc = "学校名称"),
                'logo_url': CharField(desc = "学校logo"),
                'content': CharField(desc = "学校描述"),
                'province': CharField(desc = "学校所在省"),
                'city': CharField(desc = "学校所在市"),
                'is_hot': BooleanField(desc = "是否热门"),
                'create_time': DatetimeField(desc = "创建时间"),
            }
        )
    )

    @classmethod
    def get_desc(cls):
        return "学校搜索接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        school_spliter = UniversityServer.search_school(
             request.current_page,
             **request.search_info
        )
        return school_spliter

    def fill(self, response, school_spliter):
        data_list = [{
                        "id":school.id,
                        "name":school.name,
                        "logo_url":school.logo_url,
                        "content":school.content,
                        "province":school.province,
                        "city":school.city,
                        "is_hot":school.is_hot,
                        "create_time":school.create_time,
                      }  for school in school_spliter.data]
        response.data_list = data_list
        response.total = school_spliter.total
        response.total_page = school_spliter.total_page
        return response


class SearchAll(StaffAuthorizedApi):
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
                'logo_url': CharField(desc = "学校logo"),
                'content': CharField(desc = "学校描述"),
                'province': CharField(desc = "学校所在省"),
                'city': CharField(desc = "学校所在市"),
                'is_hot': BooleanField(desc = "是否热门"),
                'create_time': DatetimeField(desc = "创建时间"),
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
                "logo_url":school.logo_url,
                "content":school.content,
                "province":school.province,
                "city":school.city,
                "is_hot":school.is_hot,
                "create_time":school.create_time,
              }  for school in school_list]
        response.data_list = data_list
        return response


class Add(StaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.school_info = RequestField(
        DictField,
        desc = "学校信息",
        conf = {
                'name': CharField(desc = "学校名称"),
                'logo_url': CharField(desc = "学校logo"),
                'content': CharField(desc = "学校描述"),
                'province': CharField(desc = "学校所在省"),
                'city': CharField(desc = "学校所在市"),
                'is_hot': BooleanField(desc = "是否热门"),
        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.school_id = ResponseField(IntField, desc = "品牌ID")

    @classmethod
    def get_desc(cls):
        return "学校创建接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        if UniversityServer.is_exsited_school(request.school_info["name"]):
            raise BusinessError("此学校已存在")
        school = UniversityServer.create_school(**request.school_info)
        return school

    def fill(self, response, school):
        response.school_id = school.id
        return response


class Update(StaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.school_id = RequestField(IntField, desc = "学校id")
    request.school_info = RequestField(
        DictField,
        desc = "需要更新的学校信息",
        conf = {
                'name': CharField(desc = "学校名称"),
                'logo_url': CharField(desc = "学校logo"),
                'content': CharField(desc = "学校描述"),
                'province': CharField(desc = "学校所在省"),
                'city': CharField(desc = "学校所在市"),
                'is_hot': BooleanField(desc = "是否热门"),
        }
    )

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "学校更新接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        school = UniversityServer.get_school(request.school_id)
        UniversityServer.update_school(school, **request.school_info)

    def fill(self, response):
        return response


class Remove(StaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.school_id = RequestField(IntField, desc = "学校id")

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "学校删除接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        school = UniversityServer.get_school(request.school_id)
        goods_qs = GoodsServer.search_all_goods(school_id = school.id)
        if goods_qs.count() > 0:
            raise BusinessError("学校已绑定商品禁止删除")
        school.delete()

    def fill(self, response):
        return response


class Settop(StaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.school_id = RequestField(IntField, desc = "学校id")

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "学校置顶接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        school = UniversityServer.get_school(request.school_id)
        is_hot = True
        if school.is_hot:
            is_hot = False
        school.update(is_hot = is_hot)

    def fill(self, response):
        return response