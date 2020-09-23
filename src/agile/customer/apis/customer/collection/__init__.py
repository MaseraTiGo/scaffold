# coding=UTF-8
import json
from infrastructure.core.field.base import CharField, DictField, \
        IntField, ListField, BooleanField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet


from infrastructure.core.exception.business_error import BusinessError
from agile.customer.manager.api import CustomerAuthorizedApi
from abs.services.agent.goods.manager import GoodsServer
from abs.middleground.business.production.manager import ProductionServer
from abs.middleground.business.merchandise.manager import MerchandiseServer
from abs.services.crm.university.manager import UniversityServer, UniversityYearsServer
from abs.services.agent.agent.manager import AgentServer
from abs.services.customer.personal.manager import CollectionRecordServer


class Search(CustomerAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc = "当前页码")
    request.search_info = RequestField(
        DictField,
        desc = "搜索收藏商品",
        conf = {
        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(
        ListField,
        desc = "商品列表",
        fmt = DictField(
            desc = "商品信息",
            conf = {
                'id': IntField(desc = "商品id"),
                'thumbnail': CharField(desc = "缩略图"),
                'title': CharField(desc = "标题"),
                'school_name': CharField(desc = "学校名称"),
                'major_name': CharField(desc = "专业名称"),
                'duration': CharField(desc = "学年"),
                'category': CharField(desc = "类别"),
                'school_city': CharField(desc = "学校所在城市"),
                'production_name': CharField(desc = "产品名称"),
                'brand_name': CharField(desc = "品牌名"),
                'sale_price': IntField(desc = "售价"),
                'agent_name': CharField(desc = "代理商名称"),
            }
        )
    )
    response.total = ResponseField(IntField, desc = "数据总数")
    response.total_page = ResponseField(IntField, desc = "总页码数")

    @classmethod
    def get_desc(cls):
        return "收藏商品列表"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        customer = self.auth_user
        request.search_info.update({
            "customer":customer,
            "is_delete":False,
        })
        page_list = CollectionRecordServer.search(
            request.current_page,
            ** request.search_info
        )
        GoodsServer.hung_goods_byids(page_list.data)
        goods_list = []
        for record in page_list.data:
            goods = record.goods
            if goods and goods not in goods_list:
                goods_list.append(goods)

        UniversityServer.hung_major(goods_list)
        UniversityServer.hung_school(goods_list)
        MerchandiseServer.hung_merchandise(goods_list)
        merchandise_list = [goods.merchandise for goods in goods_list]
        ProductionServer.hung_production(merchandise_list)
        UniversityYearsServer.hung_years(goods_list)
        AgentServer.hung_agent(goods_list)
        return page_list, goods_list

    def fill(self, response, page_list, goods_list):
        data_list = []
        for goods in goods_list:
            slideshow = json.loads(goods.merchandise.slideshow)
            data_list.append({
                'id': goods.id,
                'thumbnail': slideshow[0] if slideshow else '',
                'title': goods.merchandise.title,
                'school_name': goods.school.name,
                'major_name': goods.major.name,
                'duration': goods.years.get_duration_display(),
                'category': goods.years.get_category_display(),
                'school_city': goods.school.city,
                'production_name': goods.merchandise.production.name,
                'brand_name': goods.merchandise.production.brand.name,
                'agent_name': goods.agent.name,
                'sale_price': min([
                    specification.sale_price
                    for specification in goods.merchandise.specification_list
                ]) if goods.merchandise.specification_list else 0
            })
        response.data_list = data_list
        response.total = page_list.total
        response.total_page = page_list.total_page
        return response


class Collection(CustomerAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.goods_id = RequestField(IntField, desc = "商品id")

    response = with_metaclass(ResponseFieldSet)


    @classmethod
    def get_desc(cls):
        return "商品收藏取消接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        customer = self.auth_user
        goods = GoodsServer.get_goods(request.goods_id)
        CollectionRecordServer.collection(customer, goods)

    def fill(self, response):
        return response