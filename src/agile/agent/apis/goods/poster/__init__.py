# coding=UTF-8
import json
from infrastructure.core.field.base import CharField, DictField, \
        IntField, ListField, DatetimeField, BooleanField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet
from infrastructure.core.exception.business_error import BusinessError

from agile.crm.manager.api import StaffAuthorizedApi
from abs.services.agent.goods.manager import PosterServer
from abs.services.agent.goods.manager import GoodsServer


class Add(StaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.poster_info = RequestField(
        DictField,
        desc="商品详情",
        conf={
            'phone': CharField(desc="手机号", is_required=False),
            'goods_id': IntField(desc="商品id"),
            'remark': CharField(desc="备注"),
            'specification_list': ListField(
                desc="规格列表",
                fmt=DictField(
                    desc="规格信息",
                    conf={
                        'id': IntField(desc="规格id"),
                        'sale_price': IntField(desc="价格")
                    }
                )
            )
        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.poster_id = ResponseField(IntField, desc="ID")

    @classmethod
    def get_desc(cls):
        return "海报添加接口"

    @classmethod
    def get_author(cls):
        return "xyc"

    def execute(self, request):
        goods = GoodsServer.get_goods(request.poster_info.pop('goods_id'))
        specification_list = request.poster_info.pop('specification_list')
        poster = PosterServer.add(
            specification_list,
            goods=goods,
            **request.poster_info
        )
        return poster

    def fill(self, response, poster):
        response.poster_id = poster.id
        return response
