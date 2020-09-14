# coding=UTF-8

import datetime
from support.common.maker import BaseLoader


class ParamLoader(BaseLoader):

    def generate(self):
        return [{
                    'name': '甲方企业名称',
                    'name_key': 'agent.name',
                    'key_type': 'text',
                    'default_value': 'XXXXX信息技术有限公司',
                    'actual_value_source': 'company',
                    'is_allowed': False,
                },
                {
                    'name': '甲方企业公章',
                    'name_key': 'agent.official_seal',
                    'key_type': 'image',
                    'default_value': 'XXXXX信息技术有限公司',
                    'actual_value_source': 'company',
                    'is_allowed': False,
                },
                {
                    'name': '乙方客户姓名',
                    'name_key': 'order.invoice.name',
                    'key_type': 'text',
                    'default_value': '张三',
                    'actual_value_source': 'company',
                    'is_allowed': False,
                },
                {
                    'name': '乙方客户手机号',
                    'name_key': 'order.invoice.phone',
                    'key_type': 'text',
                    'default_value': '13000000000',
                    'actual_value_source': 'company',
                    'is_allowed': False,
                },
                {
                    'name': '乙方客户身份证号码',
                    'name_key': 'order.invoice.identification',
                    'key_type': 'text',
                    'default_value': '400000000000000000',
                    'actual_value_source': 'company',
                    'is_allowed': False,
                },
                {
                    'name': '乙方客户手签姓名',
                    'name_key': 'autograph',
                    'key_type': 'image',
                    'default_value': 'XXXXX信息技术有限公司',
                    'actual_value_source': 'customer',
                    'is_allowed': False,
                },
                {
                    'name': '合同编号',
                    'name_key': 'system.number',
                    'key_type': 'text',
                    'default_value': 'sn_202000001',
                    'actual_value_source': 'system',
                    'is_allowed': False,
                }
        ]
