# coding=UTF-8
import datetime
from infrastructure.core.field.base import CharField, DictField, \
        IntField, ListField, DatetimeField, BooleanField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet
from infrastructure.core.exception.business_error import BusinessError

from agile.crm.manager.api import StaffAuthorizedApi
from abs.services.agent.goods.manager import PosterServer
from abs.services.agent.goods.manager import GoodsServer
from abs.services.agent.customer.manager import SaleChanceServer


class Add(StaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.poster_info = RequestField(
        DictField,
        desc = "商品详情",
        conf = {
            'sale_chance_id': IntField(desc = '机会id'),
            'goods_id': IntField(desc = "商品id"),
            'remark': CharField(desc = "备注", is_required = False),
            'specification_list': ListField(
                desc = "规格列表",
                fmt = DictField(
                    desc = "规格信息",
                    conf = {
                        'id': IntField(desc = "规格id"),
                        'sale_price': IntField(desc = "价格")
                    }
                )
            )
        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.url = ResponseField(CharField, desc = "url")

    @classmethod
    def get_desc(cls):
        return "海报添加接口"

    @classmethod
    def get_author(cls):
        return "xyc"

    def execute(self, request):
        sale_chance = SaleChanceServer.get(request.poster_info.pop('sale_chance_id'))
        if self.auth_user.id != sale_chance.staff_id:
            raise BusinessError('只能生成自己客户的海报')
        if sale_chance.end_time <= datetime.date.today():
            raise BusinessError('机会已过期')
        goods = GoodsServer.get_goods(request.poster_info.pop('goods_id'))
        specification_list = request.poster_info.pop('specification_list')
        poster = PosterServer.add(
            specification_list,
            goods = goods,
            phone = sale_chance.agent_customer.phone,
            staff_id = self.auth_user.id,
            **request.poster_info
        )
        return poster

    def fill(self, response, poster):
        url = "type=poster&poster_id={poster_id}".format(
            poster_id = poster.id
        )
        response.url = url
        return response
