# coding=UTF-8
import json
from infrastructure.core.field.base import CharField, DictField, ListField, \
    IntField, DatetimeField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet

from agile.customer.manager.api import CustomerAuthorizedApi
from abs.services.customer.order.manager import OrderItemServer, OrderServer
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
    response.contract_img_list = ResponseField(
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
        img_url_list = []
        for contract in contract_list:
            url_list.extend(json.loads(contract.url))
            img_url_list.extend(json.loads(contract.img_url))
        response.contract_list = url_list
        response.contract_img_list = img_url_list
        return response


class Add(CustomerAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.order_item_id = RequestField(IntField, desc="订单详情id")
    request.contract_info = RequestField(
        DictField,
        desc="合同信息",
        conf={
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
        order = OrderServer.get(order_item.order.id)

        contract_info = request.contract_info
        contract_info.update({
            'name': order.mg_order.invoice.name,
            'phone': order.mg_order.invoice.phone,
            'identification': order.mg_order.invoice.identification,
        })
        ContractServer.create(
            order_item,
            agent,
            customer_id=order.customer_id,
            **contract_info
        )

    def fill(self, response):
        return response


class Search(CustomerAuthorizedApi):
    request = with_metaclass(RequestFieldSet)

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(
        ListField,
        desc="合同列表",
        fmt=DictField(
            desc="合同信息",
            conf={
                'id': IntField(desc="id"),
                'name': CharField(desc="名称"),
                'create_time': DatetimeField(desc="创建时间"),
                'url': ListField(
                    desc="合同列表pdf",
                    fmt=CharField(desc="合同信息")
                ),
                'img_url': ListField(
                    desc="合同列表png",
                    fmt=CharField(desc="合同信息")
                )
            }
        )
    )

    @classmethod
    def get_desc(cls):
        return "我的合同列表"

    @classmethod
    def get_author(cls):
        return "xyc"

    def execute(self, request):
        data_list = ContractServer.search_all(
            customer_id=self.auth_user.id
        )
        return data_list

    def fill(self, response, data_list):
        response.data_list = [{
            'id': contract.id,
            'name': '教育合同-{name}'.format(name=contract.name),
            'create_time': contract.create_time,
            'url': json.loads(contract.url),
            'img_url': json.loads(contract.img_url)
        } for contract in data_list]
        return response

