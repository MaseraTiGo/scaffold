# coding=UTF-8

import json
from infrastructure.core.field.base import CharField, DictField, \
        IntField, ListField, DatetimeField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet

from agile.agent.manager.api import AgentStaffAuthorizedApi
from abs.services.agent.order.manager import ContractServer
from abs.services.crm.agent.manager import AgentServer


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
          'agent_id': IntField(desc = "代理商id", is_required = False),
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
                'agent_id': IntField(desc = "代理商id"),
                'agent_name': CharField(desc = "公司名称"),
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
        contract_spliter = ContractServer.search(
            request.current_page,
            **request.search_info
        )
        AgentServer.hung_agent(contract_spliter.data)
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
            'agent_id': contract.agent.id,
            'agent_name': contract.agent.name,
            'create_time':contract.create_time,
        } for contract in contract_spliter.data]
        response.data_list = data_list
        response.total = contract_spliter.total
        response.total_page = contract_spliter.total_page
        return response
