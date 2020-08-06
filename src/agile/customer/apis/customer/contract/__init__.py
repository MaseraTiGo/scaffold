# coding=UTF-8


from infrastructure.core.field.base import CharField, DictField, ListField, \
    IntField, DatetimeField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet

from agile.customer.manager.api import CustomerAuthorizedApi
from abs.services.crm.order.manager import OrderItemServer
from infrastructure.core.exception.business_error import BusinessError
from abs.services.agent.contract.manager import ContractServer


class Get(CustomerAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.order_item_id = RequestField(IntField, desc="订单详情id")

    response = with_metaclass(ResponseFieldSet)
    response.contract_list = ResponseField(
        ListField,
        desc="合同列表",
        fmt=DictField(desc="合同信息", conf={
            'url': CharField(desc="图片")
        })
    )

    @classmethod
    def get_desc(cls):
        return "合同列表"

    @classmethod
    def get_author(cls):
        return "xyc"

    def execute(self, request):
        pass

    def fill(self, response):
        response.contract_list = []
        return response


class Add(CustomerAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.order_item_id = RequestField(IntField, desc="订单详情id")
    request.contract_info = RequestField(
        DictField,
        desc="合同信息",
        conf={
            'name': CharField(desc="签署人"),
            'phone': CharField(desc="手机号"),
            'identification': CharField(desc="身份证"),
            'email': CharField(desc="邮箱"),
            'autograph': CharField(desc="签名图片")
        }
    )

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "创建合同"

    @classmethod
    def get_author(cls):
        return "xyc"

    def execute(self, request):
        order_item = OrderItemServer.get(
            request.order_item_id
        )
        if order_item.order.customer_id != self.auth_user.id:
            raise BusinessError('订单异常')
        contract_info = request.contract_info
        autograph = contract_info.pop('autograph')

        ContractServer.create(
            customer_id=order_item.order.customer_id,
            order_item_id=order_item.id,
            agent_id=order_item.order.agent_id,
        )

    def fill(self, response):
        return response
