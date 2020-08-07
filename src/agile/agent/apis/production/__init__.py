# coding=UTF-8

import json
from infrastructure.core.field.base import CharField, DictField, \
        IntField, ListField, DatetimeField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet
from infrastructure.core.exception.business_error import BusinessError
from agile.agent.manager.api import AgentStaffAuthorizedApi
from abs.middleground.business.production.manager import ProductionServer
from abs.middleground.business.enterprise.manager import EnterpriseServer


class SearchAll(AgentStaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(
        ListField,
        desc = "产品列表",
        fmt = DictField(
            desc = "产品内容",
            conf = {
                'id': IntField(desc = "产品id"),
                'name': CharField(desc = "产品名称"),
                'attribute_list': ListField(
                    desc = "属性列表",
                    fmt = DictField(
                        desc = "分类信息",
                        conf = {
                            'category': CharField(desc = "分类名称"),
                            'attribute_list': ListField(
                                desc = "分类名称",
                                fmt = DictField(
                                    desc = "属性标签",
                                    conf = {
                                        'name': CharField(desc = "属性名称"),
                                    }
                                )
                            ),
                        }
                    )
                ),
            }
        )
    )

    @classmethod
    def get_desc(cls):
        return "产品搜索"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        company = EnterpriseServer.get_crm__company()
        production_qs = ProductionServer.search_all(
            company_id=company.id,
            **{}
        )
        return production_qs

    def fill(self, response, production_qs):
        data_list = [{
            'id': production.id,
            'name': production.name,
            'attribute_list': json.loads(production.attribute_list),
        } for production in production_qs]
        response.data_list = data_list
        return response
