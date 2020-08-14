# coding=UTF-8

from infrastructure.core.field.base import CharField, DictField, \
        IntField, ListField, BooleanField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet

from agile.base.api import NoAuthorizedApi
from abs.services.crm.university.manager import UniversityServer
from abs.services.agent.goods.manager import GoodsServer
from abs.services.crm.agent.manager import AgentServer


class HotSearch(NoAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.search_info = RequestField(
        DictField,
        desc="搜索学校",
        conf={
            'name': CharField(desc="学校名称", is_required=False),
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
                'icons': CharField(desc="学校logo"),
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
            'icons': school.logo_url,
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
                'icons': CharField(desc="学校logo"),
                'name': CharField(desc="名称"),
                'content': CharField(desc="描述"),
                'agent_list': ListField(
                    desc="代理商列表",
                    fmt=DictField(
                        desc="代理商",
                        conf={
                            'id': IntField(desc="代理商id"),
                            'name': CharField(desc='代理商名称'),
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
        GoodsServer.hung_goods_forschool(page_list.data)
        goods_list = []
        for school in page_list.data:
            goods_list.extend(school.goods_list)
        AgentServer.hung_agent(goods_list)
        return page_list

    def fill(self, response, page_list):
        data_list = []
        for school in page_list.data:
            agent_list = []
            for goods in school.goods_list:
                agent_info = {
                    'id': goods.agent.id,
                    'name': goods.agent.name
                }
                if agent_info not in agent_list:
                    agent_list.append(agent_info)
            data_list.append({
                'id': school.id,
                'icons': school.logo_url,
                'name': school.name,
                'content': school.content,
                'agent_list': agent_list
            })
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
            'icons': CharField(desc="学校logo"),
            'name': CharField(desc="名称"),
            'content': CharField(desc="描述")
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
        return school

    def fill(self, response, school):
        response.school_info = {
            'id': school.id,
            'icons': school.logo_url,
            'name': school.name,
            'content': school.content
        }
        return response


class Location(NoAuthorizedApi):
    request = with_metaclass(RequestFieldSet)

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(
        ListField,
        desc="热门城市列表",
        fmt=DictField(
            desc="省",
            conf={
                'name': CharField(desc="省名"),
                'city_list': ListField(
                    desc="城市列表",
                    fmt=DictField(
                        desc="城市",
                        conf={
                            'name': CharField(desc="城市名"),
                            'initials': CharField(desc="首字母")
                        }
                    )
                )
            }
        )
    )

    @classmethod
    def get_desc(cls):
        return "热门城市列表"

    @classmethod
    def get_author(cls):
        return "xyc"

    def execute(self, request):
        city_list = UniversityServer.get_location()
        return city_list

    def fill(self, response, city_list):
        mapping = {}
        for info in city_list:
            mapping.setdefault(
                info['province'], []
            ).append(info['city'])
        data_list = []
        for key, value in mapping.items():
            data_list.append({
                'name': key,
                'city_list': [{
                    'name': item,
                    'initials': 'w'
                } for item in value]
            })
        response.data_list = data_list
        return response
