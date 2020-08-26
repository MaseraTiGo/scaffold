# coding=UTF-8

from infrastructure.core.field.base import CharField, DictField, \
        IntField, ListField, BooleanField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet

from agile.base.api import NoAuthorizedApi
from abs.services.crm.university.manager import UniversityServer
from abs.services.agent.goods.utils.constant import DurationTypes
from abs.services.crm.university.manager import UniversityRelationsServer
from abs.services.agent.goods.manager import GoodsServer
from abs.services.crm.agent.manager import AgentServer


class Get(NoAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.major_id = RequestField(
        IntField,
        desc = "专业id"
    )

    response = with_metaclass(ResponseFieldSet)
    response.major_info = ResponseField(
        DictField,
        desc = "专业详情",
        conf = {
            'id': IntField(desc = "学校id"),
            'name': CharField(desc = "名称"),
            'content': CharField(desc = "描述"),
            'icons': CharField(desc = "图片")
        }
    )

    @classmethod
    def get_desc(cls):
        return "专业详情"

    @classmethod
    def get_author(cls):
        return "xyc"

    def execute(self, request):
        major = UniversityServer.get_major(request.major_id)
        return major

    def fill(self, response, major):
        major_info = {
            'id': major.id,
            'name': major.name,
            'content': major.content,
            'icons': major.icons,
        }
        response.major_info = major_info
        return response


class All(NoAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.search_info = RequestField(
        DictField,
        desc = "搜索专业",
        conf = {
        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(
        ListField,
        desc = "专业列表",
        fmt = DictField(
            desc = "专业信息",
            conf = {
                'id': IntField(desc = "学校id"),
                'name': CharField(desc = "名称")
            }
        )
    )

    @classmethod
    def get_desc(cls):
        return "专业列表"

    @classmethod
    def get_author(cls):
        return "xyc"

    def execute(self, request):
        major_list = UniversityServer.search_all_major(**request.search_info)
        return major_list

    def fill(self, response, major_list):
        data_list = [{
            'id': major.id,
            'name': major.name
        } for major in major_list]
        response.data_list = data_list
        return response


class Search(NoAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc = "当前页码")
    request.search_info = RequestField(
        DictField,
        desc = "搜索专业",
        conf = {
            'major_name': CharField(desc = "名称", is_required = False),
            'province': CharField(desc = "学校所在省", is_required = False),
            'city': CharField(desc = "学校所在市", is_required = False)
        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(
        ListField,
        desc = "专业列表",
        fmt = DictField(
            desc = "专业信息",
            conf = {
                'id': IntField(desc = "学校id"),
                'name': CharField(desc = "名称"),
                'content': CharField(desc = "描述"),
                'icons': CharField(desc = "图片"),
                'agent_list': ListField(
                    desc = "代理商列表",
                    fmt = DictField(
                        desc = "代理商",
                        conf = {
                            'id': IntField(desc = "代理商id"),
                            'name': CharField(desc = '代理商名称'),
                        }
                    )
                )
            }
        )
    )
    response.total = ResponseField(IntField, desc = "数据总数")
    response.total_page = ResponseField(IntField, desc = "总页码数")

    @classmethod
    def get_desc(cls):
        return "专业列表"

    @classmethod
    def get_author(cls):
        return "xyc"

    def execute(self, request):
        page_list = UniversityRelationsServer.search_major_list(
            request.current_page,
            **request.search_info
        )
        page_list.data = UniversityServer.search_all_major(
            id__in = page_list.data
        )
        mapping = {}
        for major in page_list.data:
            major.agent_list = []
            mapping.update({major.id: major})
        relation_list = UniversityRelationsServer.search_all(
            major__in = page_list.data,
            **request.search_info
        )
        GoodsServer.hung_goods_forrelations(relation_list)
        goods_list = []
        for relation in relation_list:
            goods_list.extend(relation.goods_list)
        AgentServer.hung_agent(goods_list)
        for relation in relation_list:
            major = mapping.get(relation.major_id)
            for goods in relation.goods_list:
                if goods.agent not in major.agent_list:
                    major.agent_list.append(goods.agent)
        return page_list

    def fill(self, response, page_list):
        data_list = [{
            'id': major.id,
            'name': major.name,
            'content': major.content,
            'icons': major.icons,
            'agent_list': [{
                'id': agent.id,
                'name': agent.name
            } for agent in major.agent_list]
        } for major in page_list.data]
        response.data_list = data_list
        response.total = page_list.total
        response.total_page = page_list.total_page
        return response


class HotSearch(NoAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.search_info = RequestField(
        DictField,
        desc = "搜索专业",
        conf = {
            'province': CharField(desc = "学校所在省", is_required = False),
            'city': CharField(desc = "学校所在市", is_required = False)
        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(
        ListField,
        desc = "专业列表",
        fmt = DictField(
            desc = "专业信息",
            conf = {
                'id': IntField(desc = "学校id"),
                'name': CharField(desc = "名称"),
                'content': CharField(desc = "描述"),
                'icons': CharField(desc = "图片")
            }
        )
    )

    @classmethod
    def get_desc(cls):
        return "热门专业"

    @classmethod
    def get_author(cls):
        return "xyc"

    def execute(self, request):
        major_id_list = UniversityRelationsServer.search_all_major_list(
            major__is_hot=True,
            **request.search_info
        )
        major_list = UniversityServer.search_all_major(
            id__in=major_id_list
        ).order_by('create_time')
        return major_list

    def fill(self, response, major_list):
        data_list = [{
            'id': major.id,
            'name': major.name,
            'content': major.content,
            'icons': major.icons
        } for major in major_list]
        response.data_list = data_list
        return response


class Duration(NoAuthorizedApi):
    request = with_metaclass(RequestFieldSet)

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(
        ListField,
        desc = "学年列表",
        fmt = DictField(
            desc = "专业信息",
            conf = {
                'id': CharField(desc = "key"),
                'name': CharField(desc = "值")
            }
        )
    )

    @classmethod
    def get_desc(cls):
        return "学年列表"

    @classmethod
    def get_author(cls):
        return "xyc"

    def execute(self, request):
        return []

    def fill(self, response, l):
        data_list = [{
            'id': value[0],
            'name': value[1]
        } for value in DurationTypes.CHOICES]
        response.data_list = data_list
        return response
