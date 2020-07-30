# coding=UTF-8

from infrastructure.core.field.base import CharField, DictField, \
        IntField, ListField, DatetimeField, BooleanField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet
from infrastructure.core.exception.business_error import BusinessError

from agile.crm.manager.api import StaffAuthorizedApi
from abs.services.crm.university.manager import UniversityServer


class Search(StaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc="当前页面")
    request.search_info = RequestField(
        DictField,
        desc="搜索专业",
        conf={
              'name': CharField(desc="专业名称", is_required=False),
        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.total = ResponseField(IntField, desc="数据总数")
    response.total_page = ResponseField(IntField, desc="总页码数")
    response.data_list = ResponseField(
        ListField,
        desc="专业列表",
        fmt=DictField(
            desc="专业内容",
            conf={
                'id': IntField(desc="专业id"),
                'name': CharField(desc="专业名称"),
                'content': CharField(desc="专业描述"),
                'is_hot': BooleanField(desc="是否热门"),
                'create_time': DatetimeField(desc="创建时间"),
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
        major_spliter = UniversityServer.search_major(
             request.current_page,
             **request.search_info
        )
        return major_spliter

    def fill(self, response, major_spliter):
        data_list = [{
                "id":major.id,
                "name":major.name,
                "content":major.content,
                "is_hot":major.is_hot,
                "create_time":major.create_time,
              }  for major in major_spliter.data]
        response.data_list = data_list
        response.total = major_spliter.total
        response.total_page = major_spliter.total_page
        return response


class SearchAll(StaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(
        ListField,
        desc="专业列表",
        fmt=DictField(
            desc="专业内容",
            conf={
                'id': IntField(desc="专业id"),
                'name': CharField(desc="专业名称"),
                'content': CharField(desc="专业描述"),
                'is_hot': BooleanField(desc="是否热门"),
                'create_time': DatetimeField(desc="创建时间"),
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
            "content":major.content,
            "is_hot":major.is_hot,
            "create_time":major.create_time,
          }  for major in major_list]
        response.data_list = data_list
        return response


class Add(StaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.major_info = RequestField(
        DictField,
        desc="专业信息",
        conf={
            'name': CharField(desc="专业名称"),
            'content': CharField(desc="专业描述"),
            'is_hot': BooleanField(desc="是否热门"),
        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.major_id = ResponseField(IntField, desc="品牌ID")

    @classmethod
    def get_desc(cls):
        return "创建专业"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        if UniversityServer.is_exsited_major(request.major_info["name"]):
            raise BusinessError("此专业已存在")
        major = UniversityServer.create_major(**request.major_info)
        return major

    def fill(self, response, major):
        response.major_id = major.id
        return response


class Update(StaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.major_id = RequestField(IntField, desc="专业id")
    request.major_info = RequestField(
        DictField,
        desc="需要更新的专业信息",
        conf={
            'name': CharField(desc="专业名称"),
            'content': CharField(desc="专业描述"),
            'is_hot': BooleanField(desc="是否热门"),
        }
    )

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "更新专业"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        major = UniversityServer.get_major(request.major_id)
        UniversityServer.update_major(major, **request.major_info)

    def fill(self, response):
        return response


class Remove(StaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.major_id = RequestField(IntField, desc="品牌id")

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "专业信息删除接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        major = UniversityServer.get_major(request.major_id)
        major.delete()

    def fill(self, response):
        return response


class Settop(StaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.major_id = RequestField(IntField, desc="专业id")

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "专业置顶接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        major = UniversityServer.get_major(request.major_id)
        is_hot = True
        if major.is_hot:
            is_hot = False
        major.update(is_hot=is_hot)

    def fill(self, response):
        return response
