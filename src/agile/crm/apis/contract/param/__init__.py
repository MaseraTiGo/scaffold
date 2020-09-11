# coding=UTF-8

from infrastructure.core.field.base import CharField, DictField, \
        IntField, ListField, DatetimeField, BooleanField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet
from infrastructure.core.exception.business_error import BusinessError

from agile.crm.manager.api import StaffAuthorizedApi
from abs.services.crm.contract.utils.contact import ValueSource, KeyType
from abs.services.crm.contract.manager import ParamServer
from abs.services.agent.contract.manager import TemplateParamServer


class Search(StaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc = "当前页面")
    request.search_info = RequestField(
        DictField,
        desc = "搜索合同参数",
        conf = {
              'name': CharField(desc = "参数名称", is_required = False),
              'name_key': CharField(desc = "参数key", is_required = False),
        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.total = ResponseField(IntField, desc = "数据总数")
    response.total_page = ResponseField(IntField, desc = "总页码数")
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
        param_spliter = ParamServer.search(
             request.current_page,
             **request.search_info
        )
        return param_spliter

    def fill(self, response, param_spliter):
        data_list = [{
                'id': param.id,
                'name': param.name,
                'name_key': param.name_key,
                'key_type': param.key_type,
                'default_value': param.default_value,
                'actual_value_source':param.actual_value_source,
                'actual_value_key':param.actual_value_key,
                'create_time': param.create_time,
              }  for param in param_spliter.data]
        response.data_list = data_list
        response.total = param_spliter.total
        response.total_page = param_spliter.total_page
        return response


class Add(StaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.param_info = RequestField(
        DictField,
        desc = "合同参数信息",
        conf = {
                'name': CharField(desc = "参数名称"),
                'name_key': CharField(desc = "参数key值"),
                'key_type': CharField(
                    desc = "参数类型",
                    choices = KeyType.CHOICES
                ),
                'default_value': CharField(desc = "参数默认值"),
                'actual_value_source': CharField(
                    desc = "实际来源对象",
                    choices = ValueSource.CHOICES,
                    is_required = False
                ),
                'actual_value_key': CharField(
                    desc = "实际来源对象参数",
                    is_required = False
                ),
        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.param_id = ResponseField(IntField, desc = "参数id")

    @classmethod
    def get_desc(cls):
        return "合同参数添加接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        param = ParamServer.create(**request.param_info)
        return param

    def fill(self, response, param):
        response.param_id = param.id
        return response


class Update(StaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.param_id = RequestField(IntField, desc = "合同参数id")
    request.param_info = RequestField(
        DictField,
        desc = "合同参数信息",
        conf = {
                'name': CharField(desc = "参数名称"),
                'name_key': CharField(desc = "参数key值"),
                'key_type': CharField(
                    desc = "参数类型",
                    choices = KeyType.CHOICES
                ),
                'default_value': CharField(desc = "参数默认值"),
                'actual_value_source': CharField(
                    desc = "实际来源对象",
                    choices = ValueSource.CHOICES,
                    is_required = False
                ),
                'actual_value_key': CharField(
                    desc = "实际来源对象参数",
                    is_required = False
                ),
        }
    )

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "合同参数编辑接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        ParamServer.update(
            request.param_id,
            **request.param_info
        )

    def fill(self, response):
        return response


class Remove(StaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.param_id = RequestField(IntField, desc = "合同参数id")

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "合同参数删除接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        param = ParamServer.get(request.param_id)
        template_param_qs = TemplateParamServer.search_all(param_id = param.id)
        if template_param_qs.count() > 0:
            raise BusinessError("参数已被使用无法删除")
        ParamServer.remove(param)

    def fill(self, response):
        return response
