# coding=UTF-8

from infrastructure.core.field.base import CharField, DictField, \
        IntField, ListField, DatetimeField, BooleanField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet
from infrastructure.core.exception.business_error import BusinessError

from agile.crm.manager.api import StaffAuthorizedApi
from abs.middleware.config import config_middleware


class Search(StaffAuthorizedApi):
    """配置列表"""
    request = with_metaclass(RequestFieldSet)
    request.search_info = RequestField(DictField, desc = '搜索条件', conf = {
        'type_desc': CharField(desc = "类别描述", is_required = False)
    })

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(ListField, desc = '', fmt = DictField(desc = "类别", conf = {
        'type_desc': CharField(desc = "类别名称"),
        'type': CharField(desc = '类别'),
        'data': ListField(desc = "配置", fmt = DictField(desc = '配置', conf = {
            'name': CharField(desc = "名称"),
            'key': CharField(desc = "描述"),
            'value': CharField(desc = "值"),
            'value_type': CharField(desc = "值类型"),
            'option': ListField(desc = '枚举值', fmt = CharField(desc = '枚举值')),
        }))
    }))

    @classmethod
    def get_desc(cls):
        return "配置列表接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        config_data_list = config_middleware.get_all_config()
        return config_data_list

    def fill(self, response, config_data_list):
        config_mapping = {}
        for config in config_data_list:
            if config.type != "encryption":
                if config.type not in config_mapping:
                    config_mapping[config.type] = {}
                    config_mapping[config.type]["type_desc"] = config.type_desc
                    config_mapping[config.type]["type"] = config.type
                    config_mapping[config.type]["data"] = [{"name":config.name, \
                                                            "key":config.key, \
                                                            "value":config.value, \
                                                            "value_type":config.value_type, \
                                                            "option":config.option}]
                else:
                    config_mapping[config.type]["data"].append({"name":config.name, \
                                                                "key":config.key, \
                                                                "value":config.value, \
                                                                "value_type":config.value_type, \
                                                                "option":config.option})

        response.data_list = list(config_mapping.values())
        return response


class Update(StaffAuthorizedApi):
    """配置修改"""
    request = with_metaclass(RequestFieldSet)
    request.type = RequestField(CharField, desc = '类别')
    request.key = RequestField(CharField, desc = 'key')
    request.update_info = RequestField(DictField, desc = '修改信息', conf = {
          'value': CharField(desc = "值")
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "配置修改接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        config = config_middleware.get_config(request.type, request.key)
        if config is not None:
            if config.update(**request.update_info):
                config_middleware.update_value(request.type, request.key, config.value)
            else:
                raise BusinessError('修改配置失败')
        else:
            raise BusinessError('该配置不存在')

    def fill(self, response):
        return response
