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
from abs.services.agent.goods.manager import GoodsServer
from abs.middleground.business.merchandise.manager import MerchandiseServer
from abs.services.crm.university.manager import UniversityServer


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
                'brand_name': CharField(desc = "品牌名称"),
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
            company_id = company.id,
            **{}
        )
        return production_qs

    def fill(self, response, production_qs):
        data_list = [{
            'id': production.id,
            'name': production.name,
            'brand_name': production.brand.name,
            'attribute_list': json.loads(production.attribute_list),
        } for production in production_qs]
        response.data_list = data_list
        return response


class All(AgentStaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(
        ListField,
        desc="产品列表",
        fmt=DictField(
            desc="产品信息",
            conf={
                'id': IntField(desc='产品id'),
                'name': CharField(desc="产品名称"),
                'children': ListField(
                    desc="商品列表",
                    fmt=DictField(
                        desc="商品信息",
                        conf={
                            'id': IntField(desc="商品id"),
                            'name': CharField(desc="商品名称"),
                            'major_name': CharField(desc="专业名称")
                        }
                    )
                )
            }
        )
    )

    @classmethod
    def get_desc(cls):
        return "产品商品搜索"

    @classmethod
    def get_author(cls):
        return "xyc"

    def execute(self, request):
        goods_list = list(GoodsServer.search_all_goods(
            agent_id=self.auth_user.agent_id
        ))
        MerchandiseServer.hung_merchandise(goods_list)
        ProductionServer.hung_production([goods.merchandise for goods in goods_list])
        UniversityServer.hung_major(goods_list)
        return goods_list

    def fill(self, response, goods_list):
        mapping = {}
        for goods in goods_list:
            production = goods.merchandise.production
            if production.id not in mapping:
                production.goods_list = [goods]
                mapping.update({
                    production.id: production
                })
            else:
                production = mapping.get(production.id)
                production.goods_list.append(goods)
        data_list = []
        for production in mapping.values():
            data_list.append({
                'id': production.id,
                'name': production.name,
                'children': [{
                    'id': goods.id,
                    'name': goods.merchandise.title,
                    'major_name': goods.major.name
                } for goods in goods_list]
            })
        response.data_list = data_list
        return response
