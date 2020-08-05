# coding=UTF-8

from infrastructure.core.field.base import CharField, DictField, \
        IntField, ListField, BooleanField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet

from agile.base.api import NoAuthorizedApi
from abs.middleground.business.production.manager import ProductionServer


class HotSearch(NoAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.search_info = RequestField(
        DictField,
        desc="搜索商品",
        conf={}
    )

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(
        ListField,
        desc="商品列表",
        fmt=DictField(
            desc="商品信息",
            conf={
                'id': IntField(desc="商品id"),
                'thumbnail': CharField(desc="缩略图"),
                'title': CharField(desc="标题"),
                'school_name': CharField(desc="学校名称"),
                'major_name': CharField(desc="专业名称"),
                'duration': CharField(desc="学年"),
                'school_city': CharField(desc="学校所在城市"),
                'production_name': CharField(desc="产品名称"),
                'brand_name': CharField(desc="品牌名"),
                'sale_price': IntField(desc="售价")
            }
        )
    )

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
        page_list = GoodsServer.search_enable_goods(
            request.current_page,
            **search_info
        )
        UniversityServer.hung_major(page_list.data)
        UniversityServer.hung_school(page_list.data)
        MerchandiseServer.hung_merchandise(page_list.data)
        merchandise_list = [goods.merchandise for goods in page_list.data]
        ProductionServer.hung_production(merchandise_list)
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
                'duration': goods.get_duration_display(),
                'school_city': goods.school.city,
                'production_name': goods.merchandise.production.name,
                'brand_name': goods.merchandise.production.brand.name,
                'sale_price': min([
                    specification.sale_price
                    for specification in goods.merchandise.specification_list
                ]) if goods.merchandise.specification_list else 0
            })
        response.data_list = data_list
        response.total = page_list.total
        response.total_page = page_list.total_page
        return response
