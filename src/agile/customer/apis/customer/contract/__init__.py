# coding=UTF-8
import json
from infrastructure.core.field.base import CharField, DictField, ListField, \
    IntField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet

from agile.customer.manager.api import CustomerAuthorizedApi
from abs.services.customer.order.manager import OrderItemServer
from infrastructure.core.exception.business_error import BusinessError
from abs.services.customer.order.manager import ContractServer
from abs.services.crm.agent.manager import AgentServer


class Get(CustomerAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.order_item_id = RequestField(IntField, desc="订单详情id")

    response = with_metaclass(ResponseFieldSet)
    response.contract_list = ResponseField(
        ListField,
        desc="合同列表",
        fmt=CharField(desc="合同信息")
    )

    @classmethod
    def get_desc(cls):
        return "合同列表"

    @classmethod
    def get_author(cls):
        return "xyc"

    def execute(self, request):
        order_item = OrderItemServer.get(
            request.order_item_id
        )
        if order_item.order.customer_id != self.auth_user.id:
            raise BusinessError('订单异常')
        contract_list = ContractServer.search_all(
            order_item_id=order_item.id
        )
        return contract_list

    def fill(self, response, contract_list):
        url_list = []
        for contract in contract_list:
            url_list.extend(json.loads(contract.url))
        response.contract_list = url_list
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
        agent = AgentServer.get(order_item.order.agent_id)

        contract_info = request.contract_info
        ContractServer.create(
            order_item,
            agent,
            customer_id=order_item.order.customer_id,
            **contract_info
        )
        order_item.order.invoice.update(
            name=contract_info['name'],
            phone=contract_info['phone'],
            identification=contract_info['identification']
        )

    def fill(self, response):
        return response
