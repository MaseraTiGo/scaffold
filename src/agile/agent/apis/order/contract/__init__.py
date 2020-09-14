# coding=UTF-8

import json
from infrastructure.core.field.base import CharField, DictField, \
        IntField, ListField, DatetimeField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet

from agile.agent.manager.api import AgentStaffAuthorizedApi
from infrastructure.core.exception.business_error import BusinessError
from abs.middleware.email import email_middleware
from abs.middleground.business.order.utils.constant import OrderStatus
from abs.services.agent.order.utils.constant import ContractStatus
from abs.services.agent.order.manager import OrderItemServer, ContractServer
from abs.services.agent.staff.manager import AgentStaffServer
from abs.services.agent.event.manager import StaffOrderEventServer
from abs.services.agent.contract.manager import TemplateServer, \
     TemplateParamServer


class Search(AgentStaffAuthorizedApi):
    """
    搜索合同
    """
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(
        IntField,
        desc = "当前页码"
    )
    request.search_info = RequestField(
        DictField,
        desc = "合同搜索条件",
        conf = {
          'name': CharField(desc = "签署人姓名", is_required = False),
        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.total = ResponseField(IntField, desc = "数据总数")
    response.total_page = ResponseField(IntField, desc = "总页码数")
    response.data_list = ResponseField(
        ListField,
        desc = "合同列表",
        fmt = DictField(
            desc = "合同详情",
            conf = {
                'id': IntField(desc = "合同id"),
                'name': CharField(desc = "签署人姓名"),
                'phone': CharField(desc = "签署人手机号"),
                'email':CharField(desc = "签署人邮箱"),
                'identification': CharField(desc = "签署人身份证号"),
                'url': ListField(
                    desc = 'url',
                    fmt = CharField(desc = "合同地址")
                ),
                'status': CharField(desc = "合同状态"),
                'status_name': CharField(desc = "合同状态名称"),
                'send_email_number': IntField(desc = "发送合同次数"),
                'create_time': DatetimeField(desc = "签署时间"),
            }
        )
    )
    response.total = ResponseField(IntField, desc = "数据总数")
    response.total_page = ResponseField(IntField, desc = "总页码数")

    @classmethod
    def get_desc(cls):
        return "合同搜索接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        auth = self.auth_user
        agent = self.auth_agent
        if not auth.is_admin:
            permission = AgentStaffServer.get_permission(
                auth, agent
            )
            order_ids = StaffOrderEventServer.get_order_ids(
                staff_id__in = permission.staff_ids
            )
            request.search_info.update({
                "order_id__in":order_ids
            })
        request.search_info.update({
            "agent_id":auth.agent_id
        })
        contract_spliter = ContractServer.search(
            request.current_page,
            **request.search_info
        )
        return contract_spliter

    def fill(self, response, contract_spliter):
        data_list = [{
            'id': contract.id,
            'name': contract.name,
            'phone': contract.phone,
            'email':contract.email,
            'identification':contract.identification,
            'url': json.loads(contract.url),
            'status': contract.status,
            'status_name': contract.get_status_display(),
            'send_email_number': contract.send_email_number,
            'create_time':contract.create_time,
        } for contract in contract_spliter.data]
        response.data_list = data_list
        response.total = contract_spliter.total
        response.total_page = contract_spliter.total_page
        return response


class Send(AgentStaffAuthorizedApi):
    """给客户发送邮件"""
    request = with_metaclass(RequestFieldSet)
    request.contract_id = RequestField(IntField, desc = "合同id")

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "合同发送邮件接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        ContractServer.send_email(request.contract_id)

    def fill(self, response):
        return response


class Add(AgentStaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.order_item_id = RequestField(IntField, desc = "订单详情id")
    request.contract_info_list = RequestField(
        ListField,
        desc = "合同内容列表",
        fmt = DictField(
            desc = "合同内容详情",
            conf = {
                'template_param_id': IntField(desc = "id"),
                'value': CharField(desc = "值")
            }
        )
    )

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
        return "Fsy"

    def execute(self, request):
        order_item = OrderItemServer.get(
            request.order_item_id
        )
        if order_item.order.status != OrderStatus.PAYMENT_FINISHED:
            raise BusinessError('订单状态异常')
        if order_item.template_id == 0:
            raise BusinessError('商品类型错误')
        template = TemplateServer.get(order_item.template_id)
        TemplateParamServer.huang_for_template([template])
        agent = self.auth_agent
        contract = ContractServer.create(
            order_item,
            agent,
            template,
            request.contract_info_list
        )
        return contract

    def fill(self, response, contract):
        response.contract_info = {
            'id': contract.id,
            'img_url': json.loads(contract.img_url)
        }
        return response


class Update(AgentStaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.contract_id = RequestField(IntField, desc = "合同id")
    request.contract_info_list = RequestField(
        ListField,
        desc = "合同内容列表",
        fmt = DictField(
            desc = "合同内容详情",
            conf = {
                'template_param_id': IntField(desc = "id"),
                'value': CharField(desc = "值")
            }
        )
    )

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
        return "合同信息更新接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        contract = ContractServer.get(request.contract_id)
        if contract.status == ContractStatus.SIGNED:
            raise BusinessError('已签署得合同不能编辑')
        template = TemplateServer.get(contract.template_id)
        TemplateParamServer.huang_for_template([template])
        contract = ContractServer.update(
            contract,
            template,
            request.contract_info_list
        )
        return contract

    def fill(self, response, contract):
        response.contract_info = {
            'id': contract.id,
            'img_url': json.loads(contract.img_url)
        }
        return response



class Get(AgentStaffAuthorizedApi):
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
            'data_list':ListField(
                desc = '参数列表',
                fmt = DictField(
                    desc = "参数详情",
                    conf = {
                        'template_param_id': IntField(desc = "合同参数id"),
                        'name': CharField(desc = "参数名称"),
                        'key_type':CharField(desc = "参数类型"),
                        'value': CharField(desc = "参数值"),
                    }
                )
            ),
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
            "data_list":json.loads(contract.content)
        }
        return response
