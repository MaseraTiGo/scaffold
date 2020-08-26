# coding=UTF-8
import json
from infrastructure.core.field.base import CharField, DictField, ListField, \
    IntField, DatetimeField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet

from agile.wechat.manager.api import WechatAuthorizedApi
from abs.services.agent.order.manager import OrderItemServer, OrderServer
from infrastructure.core.exception.business_error import BusinessError
from abs.services.agent.order.manager import ContractServer
from abs.services.crm.agent.manager import AgentServer
from abs.middleground.business.order.utils.constant import OrderStatus


class Get(WechatAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.order_item_id = RequestField(IntField, desc = "订单详情id")

    response = with_metaclass(ResponseFieldSet)
    response.contract_list = ResponseField(
        ListField,
        desc = "合同列表",
        fmt = CharField(desc = "合同信息")
    )
    response.contract_img_list = ResponseField(
        ListField,
        desc = "合同列表",
        fmt = CharField(desc = "合同信息")
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
        if order_item.order.person_id != self.auth_user.person_id:
            raise BusinessError('订单异常')
        contract_list = ContractServer.search_all(
            order_item_id = order_item.id
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


class Add(WechatAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.order_item_id = RequestField(IntField, desc = "订单详情id")

    response = with_metaclass(ResponseFieldSet)
    response.contract_info = ResponseField(
        DictField,
        desc = "合同信息",
        conf = {
            'id': IntField(desc = "id"),
            'img_url': ListField(
                desc = "合同列表png",
                fmt = CharField(desc = "合同信息")
            )
        }
    )

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
        '''
        if order_item.order.person_id != self.auth_user.person_id:
            raise BusinessError('订单异常')
        if order_item.order.status != OrderStatus.PAYMENT_FINISHED:
            raise BusinessError('订单状态异常')
        '''
        agent = AgentServer.get(order_item.order.agent_id)
        contacts = AgentServer.search_all_contacts(agent = agent).first()
        if not contacts:
            raise BusinessError('代理商联系人不存在，请联系客服')
        contract = ContractServer.search_all(
            order_item_id = order_item.id
        ).first()
        if not contract:
            contract = ContractServer.create(
                order_item,
                agent,
                contacts
            )
        return contract

    def fill(self, response, contract):
        response.contract_info = {
            'id': contract.id,
            'img_url': json.loads(contract.img_url)
        }
        return response


class Autograph(WechatAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.contract_id = RequestField(IntField, desc = "合同id")
    request.contract_info = RequestField(
        DictField,
        desc = "合同信息",
        conf = {
            'email': CharField(desc = "邮箱"),
            'autograph': CharField(desc = "签名图片")
        }
    )

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "签署合同"

    @classmethod
    def get_author(cls):
        return "xyc"

    def execute(self, request):
        contract = ContractServer.get(request.contract_id)
        order_item = OrderItemServer.get(contract.order_item_id)
        contract.order_item = order_item
        ContractServer.autograph(
            contract,
            request.contract_info['autograph'],
            request.contract_info['email']
        )

    def fill(self, response):
        return response


class Search(WechatAuthorizedApi):
    request = with_metaclass(RequestFieldSet)

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(
        ListField,
        desc = "合同列表",
        fmt = DictField(
            desc = "合同信息",
            conf = {
                'id': IntField(desc = "id"),
                'name': CharField(desc = "名称"),
                'create_time': DatetimeField(desc = "创建时间"),
                'url': ListField(
                    desc = "合同列表pdf",
                    fmt = CharField(desc = "合同信息")
                ),
                'img_url': ListField(
                    desc = "合同列表png",
                    fmt = CharField(desc = "合同信息")
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
            person_id = self.auth_user.person_id
        ).exclude(autograph = '').order_by('-create_time')
        return data_list

    def fill(self, response, data_list):
        response.data_list = [{
            'id': contract.id,
            'name': '教育合同-{name}'.format(name = contract.name),
            'create_time': contract.create_time,
            'url': json.loads(contract.url),
            'img_url': json.loads(contract.img_url)
        } for contract in data_list]
        return response

