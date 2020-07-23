# coding=UTF-8

'''
Created on 2020年6月30日

@author: Roy
'''

from infrastructure.core.field.base import CharField, IntField, \
        DictField, ListField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet

from infrastructure.core.exception.business_error import BusinessError
from agile.customer.manager.api import CustomerAuthorizedApi
from abs.middleground.business.person.manager import PersonServer
from abs.middleware.extend.yunaccount import yunaccount_extend


class Add(CustomerAuthorizedApi):

    request = with_metaclass(RequestFieldSet)
    request.bankcard_info = RequestField(DictField, desc="银行卡", conf={
        'name': CharField(desc="姓名"),
        'bank_number': CharField(desc="银行卡号"),
        'phone': CharField(desc="手机号"),
        'identification': CharField(desc="身份证"),
        'code': CharField(desc="验证码"),
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "添加客户银行卡"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        customer = self.auth_user
        PersonServer.add_bankcard(
            customer.person_id,
            **request.bankcard_info
        )

    def fill(self, response):
        return response


class Get(CustomerAuthorizedApi):

    request = with_metaclass(RequestFieldSet)
    request.bankcard_id = RequestField(IntField, desc="银行卡ID")

    response = with_metaclass(ResponseFieldSet)
    response.bankcard_info = ResponseField(DictField, desc="银行卡详情", conf={
        'id': IntField(desc="银行卡id"),
        'name': CharField(desc="姓名"),
        'bank_code': CharField(desc="银行编码"),
        'bank_name': CharField(desc="银行名称"),
        'bank_number': CharField(desc="银行卡号"),
        'phone': CharField(desc="手机号"),
        'identification': CharField(desc="身份证"),
    })

    @classmethod
    def get_desc(cls):
        return "获取银行卡信息"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        return PersonServer.get_bankcard(request.bankcard_id)

    def fill(self, response, bankcard):
        response.bankcard_info = {
            'id': bankcard.id,
            'name': bankcard.name,
            'identification': bankcard.identification,
            'bank_number': bankcard.bank_number,
            'bank_name': bankcard.bank_name,
            'bank_code': bankcard.bank_code,
            'phone': bankcard.phone,
        }
        return response


class All(CustomerAuthorizedApi):

    request = with_metaclass(RequestFieldSet)

    response = with_metaclass(ResponseFieldSet)
    response.bankcard_list = ResponseField(
        ListField,
        desc="银行卡列表",
        fmt=DictField(
            desc="银行卡详情",
            conf={
                'id': IntField(desc="银行卡id"),
                'name': CharField(desc="姓名"),
                'bank_code': CharField(desc="银行编码"),
                'bank_name': CharField(desc="银行名称"),
                'bank_number': CharField(desc="银行卡号"),
                'phone': CharField(desc="手机号"),
                'identification': CharField(desc="身份证"),
            }))

    @classmethod
    def get_desc(cls):
        return "客户银行卡列表"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        customer = self.auth_user
        bankcard_qs = PersonServer.get_all_bankcard(customer.person_id)
        return bankcard_qs

    def fill(self, response, bankcard_qs):
        response.bankcard_list = [{
            'id': bankcard.id,
            'name': bankcard.name,
            'identification': bankcard.identification,
            'bank_number': bankcard.bank_number,
            'bank_name': bankcard.bank_name,
            'bank_code': bankcard.bank_code,
            'phone': bankcard.phone,
        } for bankcard in bankcard_qs]
        return response


class Remove(CustomerAuthorizedApi):

    request = with_metaclass(RequestFieldSet)
    request.bankcard_id = RequestField(IntField, desc="银行卡ID")

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "删除银行卡信息"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        PersonServer.remove_bankcard(request.bankcard_id)

    def fill(self, response):
        return response
