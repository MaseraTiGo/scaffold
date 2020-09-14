# coding=UTF-8
import json
from infrastructure.core.field.base import CharField, DictField, \
        IntField, ListField, DatetimeField, BooleanField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet
from infrastructure.core.exception.business_error import BusinessError
from agile.agent.manager.api import AgentStaffAuthorizedApi
from abs.services.agent.contract.utils.constant import TemplateStatus
from abs.services.crm.contract.utils.constant import ValueSource, KeyType
from abs.services.crm.contract.manager import ParamServer
from abs.services.agent.contract.manager import TemplateServer, \
     TemplateParamServer
from abs.middleware.contract import contract_middleware
from abs.services.agent.order.manager import OrderServer, OrderItemServer


class SearchAll(AgentStaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(
        ListField,
        desc = "合同参数列表",
        fmt = DictField(
            desc = "合同参数内容",
            conf = {
                'id': IntField(desc = "参数id"),
                'name': CharField(desc = "参数名称"),
                'name_key': CharField(desc = "参数key值"),
                'key_type':CharField(
                    desc = "参数类型",
                    choices = KeyType.CHOICES
                ),
                'default_value': CharField(desc = "参数默认值"),
                'actual_value_source': CharField(
                    desc = "实际来源对象",
                    choices = ValueSource.CHOICES
                ),
                'create_time': DatetimeField(desc = "创建时间"),
            }
        )
    )

    @classmethod
    def get_desc(cls):
        return "合同参数搜索"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        param_list = ParamServer.search_all()
        return param_list

    def fill(self, response, param_list):
        data_list = [{
                'id': param.id,
                'name': param.name,
                'name_key': param.name_key,
                'key_type': param.key_type,
                'default_value': param.default_value,
                'actual_value_source':param.actual_value_source,
                'create_time': param.create_time,
              }  for param in param_list]
        response.data_list = data_list
        return response


class Get(AgentStaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.order_item_id = RequestField(IntField, desc = "订单详情id")

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(
        ListField,
        desc = "合同参数列表",
        fmt = DictField(
            desc = "合同参数内容",
            conf = {
                'template_param_id': IntField(desc = "合同参数id"),
                'name': CharField(desc = "参数名称"),
                'key_type':CharField(desc = "参数类型"),
                'value': CharField(desc = "参数值"),
            }
        )
    )

    @classmethod
    def get_desc(cls):
        return "合同填写参数查询"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        agent = self.auth_agent
        order_item = OrderItemServer.get(request.order_item_id)
        template = TemplateServer.get(order_item.template_id)
        if template.status != TemplateStatus.ADOPT:
            raise BusinessError("此合同存在异常")
        order = OrderServer.get(order_item.order_id)
        TemplateParamServer.huang_for_template([template])
        return template, order.mg_order, agent

    def fill(self, response, template, order, agent):
        data_list = []
        for template_param in template.param_list:
            param_info = json.loads(template_param.content)
            if param_info["actual_value_source"] == ValueSource.COMPANY:
                data_list.append({
                'template_param_id': template_param.id,
                'name': param_info["name"],
                'key_type': param_info["key_type"],
                'value':contract_middleware.\
                        get_contract_value(
                            order,
                            agent,
                            param_info["name_key"]
                        )
              })
        response.data_list = data_list
        return response