# coding=UTF-8

from infrastructure.core.field.base import CharField, DictField, \
        IntField, ListField, DatetimeField, BooleanField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet
from infrastructure.core.exception.business_error import BusinessError
from infrastructure.utils.common.dictwrapper import DictWrapper
from agile.agent.manager.api import AgentStaffAuthorizedApi
from abs.services.crm.contract.utils.contact import ValueSource, KeyType
from abs.services.crm.contract.manager import ParamServer
from abs.services.agent.contract.manager import TemplateServer, \
     TemplateParamServer


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
                'actual_value_key': CharField(desc = "实际来源对象参数"),
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
                'actual_value_key':param.actual_value_key,
                'create_time': param.create_time,
              }  for param in param_list]
        response.data_list = data_list
        return response