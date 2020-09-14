# coding=UTF-8
import json
from urllib import parse
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
from abs.services.agent.order.utils.constant import ContractStatus
from abs.services.agent.contract.manager import TemplateServer, \
     TemplateParamServer


class Get(WechatAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.order_item_id = RequestField(IntField, desc = "订单详情id")

    response = with_metaclass(ResponseFieldSet)
    response.contract_info = ResponseField(
        DictField,
        desc = "合同信息",
        conf = {
            'id': IntField(desc = "id"),
            'contract_list': ListField(
                desc = "合同列表png",
                fmt = CharField(desc = "合同ptf信息")
            ),
            'contract_img_list': ListField(
                desc = "合同列表png",
                fmt = CharField(desc = "合同图片信息")
            ),
            'name': CharField(desc = "签署人姓名"),
            'phone': CharField(desc = "签署人手机号"),
            'identification': CharField(desc = "签署人身份证号"),
        }
    )

    @classmethod
    def get_desc(cls):
        return "根据订单详情查询合同接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        order_item = OrderItemServer.get(
            request.order_item_id
        )
        if order_item.order.person_id != self.auth_user.person_id:
            raise BusinessError('订单异常')
        contract = None
        contract_list = ContractServer.search_all(
            order_item_id = order_item.id
        )
        if contract_list.count() > 0:
            contract = contract_list[0]
        return contract

    def fill(self, response, contract):
        response.contract_info = {
            "id":contract.id,
            "contract_list":json.loads(contract.url),
            "contract_img_list":json.loads(contract.img_url),
            "name":contract.name,
            "phone":contract.phone,
            "identification":contract.identification,
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
        if contract.status != ContractStatus.WAIT_SIGNED:
            raise BusinessError("请不要重复签署")
        order_item = OrderItemServer.get(contract.order_item_id)
        contract.order_item = order_item
        autograph = parse.unquote(
            request.contract_info.pop('autograph')
        )
        template = TemplateServer.get(contract.template_id)
        TemplateParamServer.huang_for_template([template])
        ContractServer.autograph(
            contract,
            template,
            autograph,
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
                'contract_name': CharField(desc = "名称"),
                'create_time': DatetimeField(desc = "创建时间"),
                'url': ListField(
                    desc = "合同列表pdf",
                    fmt = CharField(desc = "合同信息")
                ),
                'img_url': ListField(
                    desc = "合同列表png",
                    fmt = CharField(desc = "合同信息")
                ),
                'status': CharField(desc = "合同状态"),
                'status_name': CharField(desc = "合同状态名称"),
                'name': CharField(desc = "签署人姓名"),
                'phone': CharField(desc = "签署人手机号"),
                'identification': CharField(desc = "签署人身份证号"),
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
            person_id = self.auth_user.person_id,
            status__in = [ContractStatus.WAIT_SIGNED, ContractStatus.SIGNED]
        ).order_by('-create_time')
        return data_list

    def fill(self, response, data_list):
        response.data_list = [{
            'id': contract.id,
            'contract_name': '教育合同-{name}'.format(name = contract.name),
            'create_time': contract.create_time,
            'url': json.loads(contract.url),
            'img_url': json.loads(contract.img_url),
            'status':contract.status,
            'status_name':contract.get_status_display(),
            'name': contract.name,
            'phone': contract.phone,
            'identification':contract.identification,
        } for contract in data_list]
        return response

