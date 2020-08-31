# coding=UTF-8
import json
from infrastructure.core.field.base import CharField, DictField, \
        IntField, ListField, BooleanField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet

from agile.base.api import NoAuthorizedApi
from abs.services.agent.goods.manager import GoodsServer
from abs.middleground.business.production.manager import ProductionServer
from abs.middleground.business.merchandise.manager import MerchandiseServer
from abs.services.crm.university.manager import UniversityServer, UniversityYearsServer
from abs.services.crm.university.utils.constant import CategoryTypes
from abs.services.crm.agent.manager import AgentServer


class Search(NoAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc = "当前页码")
    request.search_info = RequestField(
        DictField,
        desc = "搜索商品",
        conf = {
            'title': CharField(desc = "标题", is_required = False),
            'province': CharField(desc = "学校所在省", is_required = False),
            'city': CharField(desc = "学校所在市", is_required = False),
            'school_id': IntField(desc = "学校id", is_required = False),
            'major_id': IntField(desc = "专业id", is_required = False),
            'duration': CharField(desc = "学年", is_required = False),
            'production_id': IntField(desc = "产品id", is_required = False),
            'category': CharField(
                desc="类型",
                choices=CategoryTypes.CHOICES,
                is_required=False
            )
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
                'category': CharField(desc="类别"),
                'school_city': CharField(desc = "学校所在城市"),
                'production_name': CharField(desc = "产品名称"),
                'brand_name': CharField(desc = "品牌名"),
                'sale_price': IntField(desc = "售价"),
                'agent_name': CharField(desc="代理商名称"),
            }
        )
    )
    response.total = ResponseField(IntField, desc = "数据总数")
    response.total_page = ResponseField(IntField, desc = "总页码数")

    @classmethod
    def get_desc(cls):
        return "商品列表"

    @classmethod
    def get_author(cls):
        return "xyc"

    def execute(self, request):
        search_info = request.search_info
        school_info = {}
        if 'province' in search_info or 'city' in search_info:
            if 'province' in search_info:
                province = search_info.pop('province')
                school_info.update({
                    'province': province
                })
            if 'city' in search_info:
                city = search_info.pop('city')
                school_info.update({
                    'city': city
                })
            school_id_list = UniversityServer.search_school_id_list(
                **school_info
            )
            search_info.update({
                'school_id__in': school_id_list
            })
        years_info = {}
        if 'category' in search_info:
            years_info.update({
                'category': search_info.pop('category')
            })
        if 'duration' in search_info:
            years_info.update({
                'duration': search_info.pop('duration')
            })
        if years_info:
            years_id_list = UniversityYearsServer.search_id_list(
                **years_info
            )
            search_info.update({
                'years_id__in': years_id_list
            })
        page_list = GoodsServer.search_enable_goods(
            request.current_page,
            **search_info
        )
        UniversityServer.hung_major(page_list.data)
        UniversityServer.hung_school(page_list.data)
        MerchandiseServer.hung_merchandise(page_list.data)
        merchandise_list = [goods.merchandise for goods in page_list.data]
        ProductionServer.hung_production(merchandise_list)
        UniversityYearsServer.hung_years(page_list.data)
        AgentServer.hung_agent(page_list.data)
        return page_list

    def fill(self, response, page_list):
        data_list = []
        for goods in page_list.data:
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


class HotSearch(NoAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.search_info = RequestField(
        DictField,
        desc = "搜索商品",
        conf = {
            'province': CharField(desc = "学校所在省", is_required = False),
            'city': CharField(desc = "学校所在市", is_required = False),
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
                'school_city': CharField(desc = "学校所在城市"),
                'production_name': CharField(desc = "产品名称"),
                'brand_name': CharField(desc = "品牌名称"),
                'agent_name': CharField(desc="代理商名称"),
                'sale_price': IntField(desc = "售价")
            }
        )
    )

    @classmethod
    def get_desc(cls):
        return "热门商品列表"

    @classmethod
    def get_author(cls):
        return "xyc"

    def execute(self, request):
        search_info = request.search_info
        school_info = {}
        if 'province' in search_info or 'city' in search_info:
            if 'province' in search_info:
                province = search_info.pop('province')
                school_info.update({
                    'province': province
                })
            if 'city' in search_info:
                city = search_info.pop('city')
                school_info.update({
                    'city': city
                })
            school_id_list = UniversityServer.search_school_id_list(
                **school_info
            )
            search_info.update({
                'school_id__in': school_id_list
            })
        data_list = GoodsServer.search_hot_goods(
            **search_info
        )
        UniversityServer.hung_major(data_list)
        UniversityServer.hung_school(data_list)
        MerchandiseServer.hung_merchandise(data_list)
        merchandise_list = [goods.merchandise for goods in data_list]
        ProductionServer.hung_production(merchandise_list)
        UniversityYearsServer.hung_years(data_list)
        AgentServer.hung_agent(data_list)
        return data_list

    def fill(self, response, data_list):
        result_list = []
        for goods in data_list:
            slideshow = json.loads(goods.merchandise.slideshow)
            result_list.append({
                'id': goods.id,
                'thumbnail': slideshow[0] if slideshow else '',
                'title': goods.merchandise.title,
                'school_name': goods.school.name,
                'major_name': goods.major.name,
                'duration': goods.years.get_duration_display(),
                'school_city': goods.school.city,
                'production_name': goods.merchandise.production.name,
                'brand_name': goods.merchandise.production.brand.name,
                'agent_name': goods.agent.name,
                'sale_price': min([
                    specification.sale_price
                    for specification in goods.merchandise.specification_list
                ]) if goods.merchandise.specification_list else 0
            })
        response.data_list = result_list
        return response


class Get(NoAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.goods_id = RequestField(IntField, desc = "商品id")

    response = with_metaclass(ResponseFieldSet)
    response.goods_info = ResponseField(DictField, desc = "商品信息", conf = {
        'slideshow': ListField(desc = "轮播图", fmt = CharField(desc = "url")),
        'video_display': CharField(desc = "展示视频"),
        'detail': ListField(desc = "商品详情", fmt = CharField(desc = "url")),
        'min_price': IntField(desc = "价格"),
        'title': CharField(desc = "标题"),
        'description': CharField(desc = "描述"),
        'despatch_type': CharField(desc = "发货方式"),
        'school_city': CharField(desc = "学校城市"),
        'month_quantity': IntField(desc = "月销数量"),
        'school_name': CharField(desc = "学校名称"),
        'major_name': CharField(desc = "专业名称"),
        'duration': CharField(desc = "学年"),
        'brand_name': CharField(desc = "品牌"),
        'production_name': CharField(desc = "产品名"),
        'agent_name': CharField(desc="代理商名称"),
        'specification_list': ListField(
            desc = "规格列表",
            fmt = DictField(
                desc = "规格",
                conf = {
                    'id': IntField(desc = "id"),
                    'sale_price': IntField(desc = "价格"),
                    'stock': IntField(desc = "库存"),
                    'show_image': CharField(desc = "展示图片"),
                    'specification_value_list': ListField(
                        desc = "商品规格值",
                        fmt = DictField(
                            desc = '规格值',
                            conf = {
                                'category': CharField(desc = "属性分类"),
                                'attribute': CharField(desc = "属性值")
                            }
                        )
                    )
                }
            )
        )
    })

    @classmethod
    def get_desc(cls):
        return "商品详情"

    @classmethod
    def get_author(cls):
        return "xyc"

    def execute(self, request):
        goods = GoodsServer.get_goods(request.goods_id)
        UniversityServer.hung_major([goods])
        UniversityServer.hung_school([goods])
        MerchandiseServer.hung_merchandise([goods])
        ProductionServer.hung_production([goods.merchandise])
        UniversityYearsServer.hung_years([goods])
        AgentServer.hung_agent([goods])
        return goods

    def fill(self, response, goods):
        response.goods_info = {
            'slideshow': json.loads(goods.merchandise.slideshow),
            'video_display': goods.merchandise.video_display,
            'detail': json.loads(goods.merchandise.detail),
            'min_price': min([
                specification.sale_price
                for specification in goods.merchandise.specification_list
            ]) if goods.merchandise.specification_list else 0,
            'title': goods.merchandise.title,
            'description': goods.merchandise.description,
            'despatch_type': goods.merchandise.despatch_type,
            'school_city': goods.school.city,
            'month_quantity': 0,
            'school_name': goods.school.name,
            'major_name': goods.major.name,
            'duration': goods.years.get_duration_display(),
            'brand_name': goods.merchandise.production.brand.name,
            'production_name': goods.merchandise.production.name,
            'agent_name': goods.agent.name,
            'specification_list': [{
                'id': specification.id,
                'sale_price': specification.sale_price,
                'stock': specification.stock,
                'show_image': specification.show_image,
                'specification_value_list': [{
                    'category': value.category,
                    'attribute': value.attribute
                } for value in specification.specification_value_list]
            } for specification in goods.merchandise.specification_list]
        }
        return response
