# coding=UTF-8


from infrastructure.core.field.base import CharField, DictField, ListField, IntField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet

from agile.customer.manager.api import CustomerAuthorizedApi
from abs.middleground.business.person.manager import PersonServer
from abs.middleground.business.merchandise.manager import MerchandiseServer
from infrastructure.core.exception.business_error import BusinessError
from abs.services.crm.production.manager import GoodsServer


class Add(CustomerAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.order_info = RequestField(DictField, desc="订单详情", conf={
        'address_id': IntField(desc="收货地址id"),
        'goods_list': ListField(
            desc='商品列表',
            fmt=DictField(
                desc='商品信息',
                conf={
                    'quantity': IntField(desc="购买数量"),
                    'specification_id': IntField(desc="规格id")
                }
            )
        )
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "客户下单接口"

    @classmethod
    def get_author(cls):
        return "xyc"

    def execute(self, request):
        order_info = request.order_info
        customer = self.auth_user
        address = PersonServer.get_address(order_info.pop('address_id'))
        specification_list = []
        merchandise_list = []
        for goods_info in order_info['goods_info']:
            specification = MerchandiseServer.get_specification(goods_info['specification_id'])
            if specification.stock < goods_info['quantity']:
                raise BusinessError('库存不足')
            if specification.merchandise.use_status != 'enable':
                raise BusinessError('商品已下架')
            merchandise_list.append(specification.merchandise)
            specification_list.append(specification)
        GoodsServer.hung_goods(merchandise_list)


    def fill(self, response):
        return response
