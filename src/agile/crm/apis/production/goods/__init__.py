# coding=UTF-8
import json
from infrastructure.core.field.base import CharField, DictField, \
        IntField, ListField, DatetimeField, BooleanField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet
from infrastructure.core.exception.business_error import BusinessError

from agile.crm.manager.api import StaffAuthorizedApi
from abs.services.crm.university.utils.constant import DurationTypes, \
     CategoryTypes
from abs.middleground.business.merchandise.utils.constant import\
     DespatchService, UseStatus
from abs.middleground.business.merchandise.manager import MerchandiseServer
from abs.middleground.business.production.manager import ProductionServer
from abs.services.agent.goods.manager import GoodsServer
from abs.services.crm.university.manager import UniversityServer, \
     UniversityYearsServer
from abs.services.crm.agent.manager import AgentServer


class Get(StaffAuthorizedApi):

    request = with_metaclass(RequestFieldSet)
    request.goods_id = RequestField(IntField, desc = "商品id")


    response = with_metaclass(ResponseFieldSet)
    response.goods_info = ResponseField(
        DictField,
        desc = "商品详情",
        conf = {
            'title': CharField(desc = "标题"),
            'video_display': CharField(desc = "宣传视频"),
            'slideshow': ListField(
                desc = '轮播图',
                fmt = CharField(desc = "图片地址")
            ),
            'detail': ListField(
                desc = '详情页',
                fmt = CharField(desc = "图片地址")
            ),
            'market_price': IntField(desc = "市场价, 单位:分"),
            'despatch_type': CharField(
                desc = "发货方式",
                choices = DespatchService.CHOICES
            ),
            'production_id': IntField(desc = "产品ID"),
            'production_name': CharField(desc = "产品ID"),
            'school_id': IntField(desc = "学校ID"),
            'school_name': CharField(desc = "学校名称"),
            'major_id': IntField(desc = "专业ID"),
            'major_name': CharField(desc = "专业名称"),
            'description': CharField(desc = "商品描述"),
            'years_id': IntField(desc = "学年ID"),
            'duration':CharField(
                desc = "时长",
                choices = DurationTypes.CHOICES
            ),
            'category':CharField(
                desc = "分类",
                choices = CategoryTypes.CHOICES
            ),
            "use_status":CharField(
                desc = "上下架",
                choices = UseStatus.CHOICES,
            ),
            'remark': CharField(desc = "备注"),
            'specification_list': ListField(
                    desc = "规格列表",
                    fmt = DictField(
                        desc = "规格详情",
                        conf = {
                            'id': IntField(desc = "规格id"),
                            'show_image': CharField(desc = "图片"),
                            'sale_price': IntField(desc = "销售价/分"),
                            'stock': IntField(desc = "库存"),
                            "specification_value_list": ListField(
                                desc = "属性值列表",
                                fmt = DictField(
                                    desc = "属性详情",
                                    conf = {
                                        "category": CharField(desc = "属性分类"),
                                        "attribute": CharField(desc = "属性值"),
                                    }
                                )
                            ),
                        }
                    )
            )
        }
    )

    @classmethod
    def get_desc(cls):
        return "商品信息查询接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        goods = GoodsServer.get_goods(request.goods_id)
        UniversityServer.hung_school([goods])
        UniversityServer.hung_major([goods])
        MerchandiseServer.hung_merchandise([goods])
        ProductionServer.hung_production([goods.merchandise])
        UniversityYearsServer.hung_years([goods])
        return goods

    def fill(self, response, goods):
        response.goods_info = {
            'id': goods.id,
            'title': goods.merchandise.title,
            'video_display': goods.merchandise.video_display,
            'slideshow': json.loads(goods.merchandise.slideshow),
            'detail': json.loads(goods.merchandise.detail),
            'market_price': goods.merchandise.market_price,
            'despatch_type': goods.merchandise.despatch_type,
            'production_id': goods.merchandise.production.id,
            'production_name': goods.merchandise.production.name,
            'school_id': goods.years.relations.school.id,
            'school_name': goods.years.relations.school.name,
            'major_id':goods.years.relations.major.id,
            'major_name': goods.years.relations.major.name,
            'description': goods.merchandise.description,
            'years_id': goods.years.id,
            'duration':goods.years.duration,
            'category':goods.years.category,
            'use_status': goods.merchandise.use_status,
            'remark': goods.merchandise.remark,
            'specification_list':[{
                'id': specification.id,
                "show_image":specification.show_image,
                "sale_price":specification.sale_price,
                "stock":specification.stock,
                "specification_value_list":[{
                    "category":specification_value.category,
                    "attribute":specification_value.attribute
                } for specification_value in specification.specification_value_list]
            } for specification in goods.merchandise.specification_list]
        }
        return response


class Search(StaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc = "当前页面")
    request.search_info = RequestField(
        DictField,
        desc = "搜索商品",
        conf = {
            'title': CharField(desc = "标题", is_required = False),
            'province': CharField(desc = "学校所在省", is_required = False),
            'city': CharField(desc = "学校所在市", is_required = False),
            'school_id': IntField(desc = "学校id", is_required = False),
            'major_id': IntField(desc = "专业id", is_required = False),
            'agent_id': IntField(desc = "代理商id", is_required = False),
        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.total = ResponseField(IntField, desc = "数据总数")
    response.total_page = ResponseField(IntField, desc = "总页码数")
    response.data_list = ResponseField(
        ListField,
        desc = "商品列表搜索接口",
        fmt = DictField(
            desc = "商品内容",
            conf = {
                'id': IntField(desc = "编号"),
                'title': CharField(desc = "标题"),
                'slideshow': ListField(
                    desc = '轮播图',
                    fmt = CharField(desc = "图片地址")
                ),
                'use_status': CharField(
                    desc = "使用状态",
                    choices = UseStatus.CHOICES
                ),
                'production_id': IntField(desc = "产品ID"),
                'production_name': CharField(desc = "产品名称"),
                'brand_id': IntField(desc = "品牌ID"),
                'brand_name': CharField(desc = "品牌名称"),
                'school_id': IntField(desc = "学校ID"),
                'school_name': CharField(desc = "学校名称"),
                'major_id': IntField(desc = "专业ID"),
                'major_name': CharField(desc = "专业名称"),
                'is_hot':BooleanField(desc = "是否热门"),
                'years_id': IntField(desc = "学年ID"),
                'duration':CharField(
                    desc = "时长",
                    choices = DurationTypes.CHOICES
                ),
                'category':CharField(
                    desc = "分类",
                    choices = CategoryTypes.CHOICES
                ),
                'agent_id': IntField(desc = "代理商id"),
                'agent_name': CharField(desc = "公司名称"),
                'create_time': DatetimeField(desc = "创建时间"),
                'specification_list': ListField(
                    desc = "规格列表",
                    fmt = DictField(
                        desc = "规格详情",
                        conf = {
                            "id": IntField(desc = "规格id"),
                            "sale_price": IntField(desc = "销售价为，单位：分"),
                            "specification_value_list": ListField(
                                desc = "属性值列表",
                                fmt = DictField(
                                    desc = "属性详情",
                                    conf = {
                                        "category": CharField(desc = "属性分类"),
                                        "attribute": CharField(desc = "属性值"),
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
        return "商品搜索"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        school_info = {}
        if 'province' in request.search_info:
            province = request.search_info.pop('province')
            school_info.update({
                'province': province
            })
        if 'city' in request.search_info:
            city = request.search_info.pop('city')
            school_info.update({
                'city': city
            })
        if len(school_info) > 0:
            school_id_list = UniversityServer.search_school_id_list(
                **school_info
            )
            request.search_info.update({
                'school_id__in': school_id_list
            })
        spliter = GoodsServer.search_goods(
            request.current_page,
            **request.search_info
        )
        AgentServer.hung_agent(spliter.data)
        UniversityServer.hung_major(spliter.data)
        UniversityServer.hung_school(spliter.data)
        MerchandiseServer.hung_merchandise(spliter.data)
        merchandise_list = [goods.merchandise for goods in spliter.data]
        ProductionServer.hung_production(merchandise_list)
        UniversityYearsServer.hung_years(spliter.data)
        return spliter

    def fill(self, response, spliter):
        data_list = [{
            'id': goods.id,
            'title': goods.merchandise.title,
            'slideshow':json.loads(goods.merchandise.slideshow),
            'use_status': goods.merchandise.use_status,
            'production_id': goods.merchandise.production.id,
            'production_name': goods.merchandise.production.name,
            'brand_id': goods.merchandise.production.brand.id,
            'brand_name':goods.merchandise.production.brand.name,
            'school_id': goods.years.relations.school.id,
            'school_name': goods.years.relations.school.name,
            'major_id':goods.years.relations.major.id,
            'major_name': goods.years.relations.major.name,
            'is_hot':goods.is_hot,
            'years_id': goods.years.id,
            'duration':goods.years.duration,
            'category':goods.years.category,
            'agent_id': 0,
            'agent_name': goods.agent.name,
            'create_time':goods.create_time,
            'specification_list':[{
                "id": specification.id,
                "sale_price":specification.sale_price,
                "specification_value_list":[{
                    "category":specification_value.category,
                    "attribute":specification_value.attribute
                } for specification_value in specification.specification_value_list]
            } for specification in goods.merchandise.specification_list]
        } for goods in spliter.data]
        response.data_list = data_list
        response.total = spliter.total
        response.total_page = spliter.total_page
        return response


class Remove(StaffAuthorizedApi):
    """删除商品信息"""
    request = with_metaclass(RequestFieldSet)
    request.goods_id = RequestField(IntField, desc = "商品id")

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "商品信息删除接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        goods = GoodsServer.get_goods(request.goods_id)
        MerchandiseServer.remove(goods.merchandise_id)
        goods.delete()

    def fill(self, response):
        return response


class Setuse(StaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.goods_id = RequestField(IntField, desc = "商品id")

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "商品上下架接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        goods = GoodsServer.get_goods(request.goods_id)
        merchandise = MerchandiseServer.get(goods.merchandise_id)
        if len(merchandise.specification_list) == 0:
            raise BusinessError("该商品缺少规格无法上架")
        use_status = UseStatus.ENABLE
        if merchandise.use_status == UseStatus.ENABLE:
            use_status = UseStatus.FORBIDDENT
        merchandise.update(use_status = use_status)

    def fill(self, response):
        return response


class Settop(StaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.goods_id = RequestField(IntField, desc = "商品id")

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "商品置顶接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        goods = GoodsServer.get_goods(request.goods_id)
        is_hot = True
        if goods.is_hot:
            is_hot = False
        if is_hot:
           merchandise = MerchandiseServer.get(goods.merchandise_id)
           if merchandise.use_status == UseStatus.FORBIDDENT:
               raise BusinessError("请先上架商品")
        goods.update(is_hot = is_hot)

    def fill(self, response):
        return response