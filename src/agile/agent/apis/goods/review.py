# coding=UTF-8
import json

from abs.middleground.business.merchandise.manager import MerchandiseServer
from abs.middleground.business.production.manager import ProductionServer
from abs.services.agent.agent.manager import AgentServer
from abs.services.agent.goods.manager import GoodsReviewServer
from abs.services.agent.goods.manager import GoodsServer
from abs.services.agent.goods.utils.constant import ReviewStatus
from abs.services.crm.university.manager import UniversityServer, \
    UniversityYearsServer
from abs.services.crm.university.utils.constant import DurationTypes, \
    CategoryTypes
from agile.agent.manager.api import AgentStaffAuthorizedApi
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.field.base import CharField, DictField, \
    IntField, ListField, DatetimeField, BooleanField


class Search(AgentStaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc="当前页面")
    request.search_info = RequestField(
        DictField,
        desc="搜索商品",
        conf={
            'title': CharField(desc="标题", is_required=False),
            'status': CharField(desc="审核状态", is_required=False,
                                choices=ReviewStatus.CHOICES),
        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.total = ResponseField(IntField, desc="数据总数")
    response.total_page = ResponseField(IntField, desc="总页码数")
    response.data_list = ResponseField(
        ListField,
        desc="商品审核列表搜索接口",
        fmt=DictField(
            desc="商品内容",
            conf={
                'id': IntField(desc="编号"),
                'title': CharField(desc="标题"),
                'slideshow': ListField(
                    desc='轮播图',
                    fmt=CharField(desc="图片地址")
                ),
                'status': CharField(
                    desc="审核状态",
                    choices=ReviewStatus.CHOICES
                ),
                'production_id': IntField(desc="产品ID"),
                'remark': CharField(desc="审核备注"),
                'production_name': CharField(desc="产品名称"),
                'brand_id': IntField(desc="品牌ID"),
                'brand_name': CharField(desc="品牌名称"),
                'school_id': IntField(desc="学校ID"),
                'school_name': CharField(desc="学校名称"),
                'major_id': IntField(desc="专业ID"),
                'major_name': CharField(desc="专业名称"),
                'is_hot': BooleanField(desc="是否热门"),
                'years_id': IntField(desc="学年ID"),
                'duration': CharField(
                    desc="时长",
                    choices=DurationTypes.CHOICES
                ),
                'category': CharField(
                    desc="分类",
                    choices=CategoryTypes.CHOICES
                ),
                'agent_id': IntField(desc="代理商id"),
                'agent_name': CharField(desc="公司名称"),
                'create_time': DatetimeField(desc="创建时间"),
                'specification_list': ListField(
                    desc="规格列表",
                    fmt=DictField(
                        desc="规格详情",
                        conf={
                            "id": IntField(desc="规格id"),
                            "sale_price": IntField(desc="销售价为，单位：分"),
                            "specification_value_list": ListField(
                                desc="属性值列表",
                                fmt=DictField(
                                    desc="属性详情",
                                    conf={
                                        "category": CharField(desc="属性分类"),
                                        "attribute": CharField(desc="属性值"),
                                    }
                                )
                            ),
                        }
                    )
                )
            }
        )
    )

    @classmethod
    def get_desc(cls):
        return "商品审核列表搜索"

    @classmethod
    def get_author(cls):
        return "djd"

    def execute(self, request):
        agent = self.auth_user
        request.search_info.update({'agent_id': agent.company_id})
        spliter = GoodsServer.search_goods(
            request.current_page,
            review=True,
            **request.search_info
        )
        AgentServer.hung_agent(spliter.data)
        UniversityServer.hung_major(spliter.data)
        UniversityServer.hung_school(spliter.data)
        MerchandiseServer.hung_merchandise(spliter.data)
        merchandise_list = [goods.merchandise for goods in spliter.data]
        ProductionServer.hung_production(merchandise_list)
        UniversityYearsServer.hung_years(spliter.data)
        GoodsReviewServer.hung_goods_review_status(spliter.data)
        return spliter

    def fill(self, response, spliter):
        data_list = [{
            'id': goods.id,
            'title': goods.merchandise.title,
            'slideshow': json.loads(goods.merchandise.slideshow),
            'status': goods.gr_status,
            'remark': goods.gr_remark,
            'production_id': goods.merchandise.production.id,
            'production_name': goods.merchandise.production.name,
            'brand_id': goods.merchandise.production.brand.id,
            'brand_name': goods.merchandise.production.brand.name,
            'school_id': goods.years.relations.school.id,
            'school_name': goods.years.relations.school.name,
            'major_id': goods.years.relations.major.id,
            'major_name': goods.years.relations.major.name,
            'is_hot': goods.is_hot,
            'years_id': goods.years.id,
            'duration': goods.years.duration,
            'category': goods.years.category,
            'agent_id': 0,
            'agent_name': goods.agent.name,
            'create_time': goods.create_time,
            'specification_list': [{
                "id": specification.id,
                "sale_price": specification.sale_price,
                "specification_value_list": [{
                    "category": specification_value.category,
                    "attribute": specification_value.attribute
                } for specification_value in specification.specification_value_list]
            } for specification in goods.merchandise.specification_list]
        } for goods in spliter.data]
        response.data_list = data_list
        response.total = spliter.total
        response.total_page = spliter.total_page
        return response


class SetStatus(AgentStaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.goods_id = RequestField(IntField, desc="商品id")

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "商品提交审核接口"

    @classmethod
    def get_author(cls):
        return "djd"

    def execute(self, request):
        review_info = {'status': 'wait_review'}
        GoodsReviewServer.set_review_result(request.goods_id, **review_info)

    def fill(self, response):
        return response
