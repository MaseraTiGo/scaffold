# coding=UTF-8

'''
Created on 2020年7月3日

@author: Roy
'''

from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet
from infrastructure.core.field.base import CharField, IntField, DictField

from agile.customer.manager.api import CustomerAuthorizedApi
from abs.services.customer.finance.manager import CustomerFinanceServer


class Get(CustomerAuthorizedApi):

    request = with_metaclass(RequestFieldSet)

    response = with_metaclass(ResponseFieldSet)
    response.balance = ResponseField(IntField, desc="余额")

    @classmethod
    def get_desc(cls):
        return "客户余额获取接口"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        balance = CustomerFinanceServer.get_balance(
            customer_id=self.auth_user.id
        )
        return balance

    def fill(self, response, balance):
        response.balance = balance
        return response


class TopUp(CustomerAuthorizedApi):

    request = with_metaclass(RequestFieldSet)
    request.amount = RequestField(IntField, desc="充值金额")
    request.pay_type = RequestField(
        CharField,
        desc="交易方式",
        choices=(
            ('bank', '银行'),
            ('alipay', "支付宝"),
            ('wechat', "微信"),
            ('balance', "余额")
        )
    )
    request.remark = RequestField(CharField, desc="充值说明")

    response = with_metaclass(ResponseFieldSet)
    response.pay_info = ResponseField(DictField, desc='支付信息', conf={
        'timestamp': CharField(desc="时间"),
        'prepayid': CharField(desc="微信预支付id"),
        'noncestr': CharField(desc="随机字符串"),
        'sign': CharField(desc="签名")
    })

    @classmethod
    def get_desc(cls):
        return "客户余额充值接口"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        prepay_id = CustomerFinanceServer.top_up(
            customer_id=self.auth_user.id,
            amount=request.amount,
            pay_type=request.pay_type,
            remark=request.remark,
        )
        pay_info = CustomerFinanceServer.parse_pay_info(prepay_id, request.pay_type)
        return pay_info

    def fill(self, response, pay_info):
        response.pay_info = pay_info
        return response


class Withdraw(CustomerAuthorizedApi):

    request = with_metaclass(RequestFieldSet)
    request.amount = RequestField(IntField, desc="提现金额")
    request.remark = RequestField(CharField, desc="提现说明")
    request.pay_type = RequestField(
        CharField,
        desc="交易方式",
        choices=(
            ('bank', '银行'),
            ('alipay', "支付宝"),
            ('wechat', "微信"),
            ('balance', "余额")
        )
    )

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "客户余额提现接口"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        CustomerFinanceServer.withdraw(
            customer_id=self.auth_user.id,
            amount=request.amount,
            pay_type=request.pay_type,
            remark=request.remark,
        )

    def fill(self, response):
        return response
