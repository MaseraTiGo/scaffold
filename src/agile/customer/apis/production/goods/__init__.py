# coding=UTF-8
import json
from infrastructure.core.field.base import CharField, DictField, \
        IntField, ListField, BooleanField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet

from agile.customer.manager.api import CustomerAuthorizedApi
from abs.services.crm.production.manager import GoodsServer


class Search(CustomerAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc="当前页码")
    request.search_info = RequestField(
        DictField,
        desc="搜索商品",
        conf={
            'title': CharField(desc="标题", is_required=False),
            'province': CharField(desc="学校所在省", is_required=False),
            'city': CharField(desc="学校所在市", is_required=False),
            'school_id': IntField(desc="学校id", is_required=False),
            'major_id': IntField(desc="专业id", is_required=False),
            'duration': CharField(desc="学年", is_required=False)
        }
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
                'sale_price': IntField(desc="售价")
            }
        )
    )
    response.total = ResponseField(IntField, desc="数据总数")
    response.total_page = ResponseField(IntField, desc="总页码数")

    @classmethod
    def get_desc(cls):
        return "商品列表"

    @classmethod
    def get_author(cls):
        return "xyc"

    def execute(self, request):
        page_list = GoodsServer.search_goods(
            request.current_page,
            **request.search_info
        )
        return page_list

    def fill(self, response, page_list):
        data_list = []
        for goods in page_list:
            slideshow = json.loads(goods.merchandise.slideshow)
            data_list.append({
                'id': goods.id,
                'thumbnail': slideshow[0] if slideshow else '',
                'title': goods.merchandise.title,
                'school_name': goods.school.name,
                'major_name': goods.major.name,
                'duration': goods.duration,
                'school_city': goods.school.city,
                'production_name': goods.merchandise.production.name,
                'sale_price': min([
                    specification.sale_price
                    for specification in goods.merchandise.specification_list
                ])
            })
        response.data_list = data_list
        return response
