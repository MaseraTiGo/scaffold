# coding=UTF-8

from infrastructure.core.field.base import CharField, DictField, \
        IntField, ListField, BooleanField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet

from agile.base.api import NoAuthorizedApi
from abs.services.crm.university.manager import UniversityServer, UniversityYearsServer
from abs.services.agent.goods.manager import GoodsServer
from abs.services.crm.agent.manager import AgentServer


class SearchMajor(NoAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc="当前页码")
    request.search_info = RequestField(
        DictField,
        desc="搜索专业",
        conf={
            'school_id': IntField(desc="学校id"),
            'category': CharField(desc="类别")
        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(
        ListField,
        desc="专业列表",
        fmt=DictField(
            desc="专业信息",
            conf={
                'id': IntField(desc="id"),
                'name': CharField(desc="专业名称"),
                'content': CharField(desc="专业描述"),
                'icons': CharField(desc="专业图片"),
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
        return "学校的专业列表"

    @classmethod
    def get_author(cls):
        return "xyc"

    def execute(self, request):
        page_list = UniversityYearsServer.search_major_list(
            request.current_page,
            **request.search_info
        )
        page_list.data = UniversityServer.search_all_major(
            id__in=page_list.data
        ).order('-is_hot', 'create_time')
        mapping = {}
        for major in page_list.data:
            major.agent_list = []
            mapping.update({
                major.id: major
            })
        years_list = UniversityYearsServer.search_all(
            relations__major__in=page_list.data,
            **request.search_info
        )
        GoodsServer.hung_goods_foryears(years_list)
        goods_list = []
        for years in years_list:
            goods_list.extend(years.goods_list)
        AgentServer.hung_agent(goods_list)
        for years in years_list:
            major = mapping.get(years.relations.major_id)
            for goods in years.goods_list:
                agent_info = {
                    'id': goods.agent.id,
                    'name': goods.agent.name
                }
                if agent_info not in major.agent_list:
                    major.agent_list.append(agent_info)
        return page_list

    def fill(self, response, page_list):
        data_list = []
        for major in page_list.data:
            data_list.append({
                'id': major.id,
                'name': major.name,
                'content': major.content,
                'icons': major.icons,
                'agent_list': major.agent_list
            })
        response.data_list = data_list
        response.total = page_list.total
        response.total_page = page_list.total_page
        return response


class SearchSchool(NoAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc="当前页码")
    request.search_info = RequestField(
        DictField,
        desc="搜索学校",
        conf={
            'major_id': IntField(desc="专业id"),
            'category': CharField(desc="类别")
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
                'name': CharField(desc="学校名称"),
                'content': CharField(desc="学校描述"),
                'icons': CharField(desc="学校logo"),
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
        return "专业的学校列表"

    @classmethod
    def get_author(cls):
        return "xyc"

    def execute(self, request):
        page_list = UniversityYearsServer.search_school_list(
            request.current_page,
            **request.search_info
        )
        page_list.data = UniversityServer.search_all_school(
            id__in=page_list.data
        ).order('-is_hot', 'create_time')
        mapping = {}
        for school in page_list.data:
            school.agent_list = []
            mapping.update({
                school.id: school
            })
        years_list = UniversityYearsServer.search_all(
            relations__school__in=page_list.data,
            **request.search_info
        )
        GoodsServer.hung_goods_foryears(years_list)
        goods_list = []
        for years in years_list:
            goods_list.extend(years.goods_list)
        AgentServer.hung_agent(goods_list)
        for years in years_list:
            school = mapping.get(years.relations.school_id)
            for goods in years.goods_list:
                agent_info = {
                    'id': goods.agent.id,
                    'name': goods.agent.name
                }
                if agent_info not in school.agent_list:
                    school.agent_list.append(agent_info)
        return page_list

    def fill(self, response, page_list):
        data_list = []
        for school in page_list.data:
            data_list.append({
                'id': school.id,
                'name': school.name,
                'content': school.content,
                'icons': school.logo_url,
                'agent_list': school.agent_list
            })
        response.data_list = data_list
        response.total = page_list.total
        response.total_page = page_list.total_page
        return response
