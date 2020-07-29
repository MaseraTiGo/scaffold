# coding=UTF-8

from infrastructure.core.field.base import CharField, DictField, \
        IntField, ListField, BooleanField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet

from agile.customer.manager.api import CustomerAuthorizedApi


class HotSearch(CustomerAuthorizedApi):
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
        school_list = []
        return school_list

    def fill(self, response, school_list):
        data_list = []
        response.data_list = data_list
        return response


class Search(CustomerAuthorizedApi):
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
        page_list = []
        return page_list

    def fill(self, response, page_list):
        data_list = []
        response.data_list = data_list
        response.total = 0
        response.total_page = 1
        return response


class All(CustomerAuthorizedApi):
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
        return "热门学校列表"

    @classmethod
    def get_author(cls):
        return "xyc"

    def execute(self, request):
        school_list = []
        return school_list

    def fill(self, response, school_list):
        data_list = []
        response.data_list = data_list
        return response