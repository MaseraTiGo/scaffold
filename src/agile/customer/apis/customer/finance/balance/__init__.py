# coding=UTF-8

'''
Created on 2020年7月3日

@author: Roy
'''

from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet
from infrastructure.core.exception.business_error import BusinessError
from infrastructure.core.field.base import CharField, DictField, IntField, ListField, DatetimeField, DateField, BooleanField

from agile.customer.manager.api import CustomerAuthorizedApi
from abs.service.customer.manager import CustomerServer, CustomerFinanceServer


class Get(CustomerAuthorizedApi):

    request = with_metaclass(RequestFieldSet)

    response = with_metaclass(ResponseFieldSet)
    response.balance = ResponseField(IntField, desc = "余额")

    @classmethod
    def get_desc(cls):
        return "客户余额获取接口"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        balance = CustomerFinanceServer.get_balance(
            customer_id = self.auth_user.id
        )
        return balance

    def fill(self, response, balance):
        response.balance = balance
        return response


class TopUp(CustomerAuthorizedApi):

    request = with_metaclass(RequestFieldSet)
    request.amount = RequestField(IntField, desc = "充值金额")
    request.pay_type = RequestField(CharField, desc = "交易方式", \
                        choices = (('bank', '银行'), ('alipay', "支付宝"), ('wechat', "微信"),
                                  ('balance', "余额")))
    request.remark = RequestField(CharField, desc = "充值说明")

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "客户余额充值接口"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        CustomerFinanceServer.top_up(
            customer_id = self.auth_user.id,
            amount = request.amount,
            pay_type = request.pay_type,
            remark = request.remark,
        )

    def fill(self, response, token):
        return response


class Withdraw(CustomerAuthorizedApi):

    request = with_metaclass(RequestFieldSet)
    request.amount = RequestField(IntField, desc = "提现金额")
    request.remark = RequestField(CharField, desc = "提现说明")
    request.pay_type = RequestField(CharField, desc = "交易方式", \
                        choices = (('bank', '银行'), ('alipay', "支付宝"), ('wechat', "微信"),
                                  ('balance', "余额")))

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "客户余额提现接口"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        CustomerFinanceServer.withdraw(
            customer_id = self.auth_user.id,
            amount = request.amount,
            pay_type = request.pay_type,
            remark = request.remark,
        )

    def fill(self, response):
        return response
