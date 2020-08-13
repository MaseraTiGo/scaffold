# coding=UTF-8

from infrastructure.core.field.base import CharField, DictField, \
        IntField, ListField, BooleanField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet

from agile.base.api import NoAuthorizedApi
from abs.services.crm.university.manager import UniversityServer


class HotSearch(NoAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.search_info = RequestField(
        DictField,
        desc="搜索学校",
        conf={
            'province': CharField(desc="学校所在省", is_required=False),
            'city': CharField(desc="学校所在市", is_required=False)
        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(
        ListField,
        desc="学校列表",
        fmt=DictField(
            desc="学校信息",
            conf={
                'id': IntField(desc="学校id"),
                'logo_url': CharField(desc="学校logo"),
                'name': CharField(desc="名称"),
                'content': CharField(desc="描述")
            }
        )
    )

    @classmethod
    def get_desc(cls):
        return "热门学校列表"

    @classmethod
    def get_author(cls):
        return "xyc"

    def execute(self, request):
        school_list = UniversityServer.search_hot_school(
            **request.search_info
        )
        return school_list

    def fill(self, response, school_list):
        data_list = [{
            'id': school.id,
            'logo_url': school.logo_url,
            'name': school.name,
            'content': school.content
        } for school in school_list]
        response.data_list = data_list
        return response


class Search(NoAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc="当前页码")
    request.search_info = RequestField(
        DictField,
        desc="搜索学校",
        conf={
            'name': CharField(desc="名称", is_required=False),
            'province': CharField(desc="学校所在省", is_required=False),
            'city': CharField(desc="学校所在市", is_required=False)
        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(
        ListField,
        desc="学校列表",
        fmt=DictField(
            desc="学校信息",
            conf={
                'id': IntField(desc="学校id"),
                'logo_url': CharField(desc="学校logo"),
                'name': CharField(desc="名称"),
                'content': CharField(desc="描述"),
                'production_list': ListField(
                    desc="产品列表",
                    fmt=DictField(
                        desc="产品信息",
                        conf={
                            'id': IntField(desc="产品id"),
                            'name': CharField(desc='产品名称'),
                            'quantity': IntField(desc="商品数量")
                        }
                    )
                )
            }
        )
    )
    response.total = ResponseField(IntField, desc="数据总数")
    response.total_page = ResponseField(IntField, desc="总页码数")

    @classmethod
    def get_desc(cls):
        return "搜索学校列表"

    @classmethod
    def get_author(cls):
        return "xyc"

    def execute(self, request):
        page_list = UniversityServer.search_school(
            request.current_page,
            **request.search_info
        )
        UniversityServer.hung_production_list(page_list.data)
        return page_list

    def fill(self, response, page_list):
        data_list = [{
            'id': school.id,
            'logo_url': school.logo_url,
            'name': school.name,
            'content': school.content,
            'production_list': sorted(
                school.production_list,
                key=lambda x: x['quantity'],
                reverse=True
            )
        } for school in page_list.data]
        response.data_list = data_list
        response.total = page_list.total
        response.total_page = page_list.total_page
        return response


class All(NoAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.search_info = RequestField(
        DictField,
        desc="搜索学校",
        conf={
            'province': CharField(desc="学校所在省", is_required=False),
            'city': CharField(desc="学校所在市", is_required=False)
        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(
        ListField,
        desc="学校列表",
        fmt=DictField(
            desc="学校信息",
            conf={
                'id': IntField(desc="学校id"),
                'name': CharField(desc="名称")
            }
        )
    )

    @classmethod
    def get_desc(cls):
        return "所有学校列表"

    @classmethod
    def get_author(cls):
        return "xyc"

    def execute(self, request):
        school_list = UniversityServer.search_all_school(**request.search_info)
        return school_list

    def fill(self, response, school_list):
        data_list = [{
            'id': school.id,
            'name': school.name
        } for school in school_list]
        response.data_list = data_list
        return response


class Get(NoAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.school_id = RequestField(IntField, desc="学校id")

    response = with_metaclass(ResponseFieldSet)
    response.school_info = ResponseField(
        DictField,
        desc="学校",
        conf={
            'id': IntField(desc="学校id"),
            'logo_url': CharField(desc="学校logo"),
            'name': CharField(desc="名称"),
            'content': CharField(desc="描述"),
            'production_list': ListField(
                desc="产品列表",
                fmt=DictField(
                    desc="产品信息",
                    conf={
                        'id': IntField(desc="产品id"),
                        'name': CharField(desc='产品名称'),
                        'quantity': IntField(desc="商品数量")
                    }
                )
            )
        }

    )

    @classmethod
    def get_desc(cls):
        return "学校详情"

    @classmethod
    def get_author(cls):
        return "xyc"

    def execute(self, request):
        school = UniversityServer.get_school(request.school_id)
        UniversityServer.hung_production_list([school])
        return school

    def fill(self, response, school):
        response.school_info = {
            'id': school.id,
            'logo_url': school.logo_url,
            'name': school.name,
            'content': school.content,
            'production_list': sorted(
                school.production_list,
                key=lambda x: x['quantity'],
                reverse=True
            )
        }
        return response


class Location(NoAuthorizedApi):
    request = with_metaclass(RequestFieldSet)

    response = with_metaclass(ResponseFieldSet)
    response.hot_city_list = ResponseField(
        ListField,
        desc="热门城市列表",
        fmt=CharField(desc="城市")
    )

    @classmethod
    def get_desc(cls):
        return "热门城市列表"

    @classmethod
    def get_author(cls):
        return "xyc"

    def execute(self, request):
        hot_city_list = UniversityServer.get_location(
            is_hot=True
        )
        return hot_city_list

    def fill(self, response, hot_city_list):
        response.hot_city_list = hot_city_list
        return response
