# coding=UTF-8

from infrastructure.core.field.base import CharField, DictField, \
        IntField, ListField, BooleanField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet

from agile.base.api import NoAuthorizedApi
from abs.services.crm.university.manager import UniversityRelationsServer
from abs.services.agent.goods.manager import GoodsServer
from abs.services.crm.agent.manager import AgentServer


class Search(NoAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc="当前页码")
    request.search_info = RequestField(
        DictField,
        desc="搜索专业",
        conf={
            'school_id': IntField(desc="学校id", is_required=False),
            'major_id': IntField(desc="专业id", is_required=False),
            'category': CharField(desc="类别", is_required=False)
        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(
        ListField,
        desc="专业列表",
        fmt=DictField(
            desc="专业信息",
            conf={
                'id': IntField(desc="学校id"),
                'major_id': IntField(desc="专业id"),
                'major_name': CharField(desc="专业名称"),
                'major_content': CharField(desc="专业描述"),
                'major_icons': CharField(desc="专业图片"),
                'school_id': IntField(desc="学校id"),
                'school_name': CharField(desc="学校名称"),
                'school_content': CharField(desc="学校描述"),
                'school_logo_url': CharField(desc="学校logo"),
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
        return "学校专业列表"

    @classmethod
    def get_author(cls):
        return "xyc"

    def execute(self, request):
        page_list = UniversityRelationsServer.search(
            request.current_page,
            **request.search_info
        )
        GoodsServer.hung_goods_forrelations(page_list.data)
        goods_list = []
        for school in page_list.data:
            goods_list.extend(school.goods_list)
        AgentServer.hung_agent(goods_list)
        return page_list

    def fill(self, response, page_list):
        data_list = [{
            'id': relation.id,
            'major_id': relation.major.id,
            'major_name': relation.major.name,
            'major_content': relation.major.content,
            'major_icons': relation.major.icons,
            'school_id': relation.school.id,
            'school_name': relation.school.name,
            'school_content': relation.school.content,
            'school_logo_url': relation.school.logo_url,
            'agent_list': list(set([{
                'id': goods.agent.id,
                'name': goods.agent.name
            } for goods in relation.goods_list]))
        } for relation in page_list.data]
        response.data_list = data_list
        response.total = page_list.total
        response.total_page = page_list.total_page
        return response
