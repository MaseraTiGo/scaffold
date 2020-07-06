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
    request.transaction_id = RequestField(IntField, desc = "交易id")

    response = with_metaclass(ResponseFieldSet)
    response.transaction_info = ResponseField(DictField, desc = "交易详情", conf = {
                                        'id': IntField(desc = "交易ID"),
                                        'number': CharField(desc = "交易编号"),
                                        'amount': IntField(desc = "交易金额"),
                                        'pay_type': CharField(desc = "交易方式"),
                                        'remark': CharField(desc = "交易说明"),
                                        'status': CharField(desc = "交易状态", choices = (\
                                                ('pay_finish', '付款成功'), \
                                                ('transaction_dealing', "交易处理中"),\
                                                ('account_finish', "到账成功"))),
                                        'create_time': DatetimeField(desc = "交易时间"),
                                    })

    @classmethod
    def get_desc(cls):
        return "客户交易详情获取接口"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        transaction = CustomerFinanceServer.get_transacation_detail(
            transaction_id = request.transaction_id
        )
        return transaction

    def fill(self, response, transaction):
        response.transaction_info = {
            'id': transaction.id,
            'number': transaction.number,
            'amount': transaction.amount,
            'pay_type': transaction.pay_type,
            'remark': transaction.remark,
            'status': transaction.record.status,
            'create_time': transaction.create_time,
        }
        return response


class Search(CustomerAuthorizedApi):

    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc = "当前页码")
    request.search_info = RequestField(DictField, desc = "搜索交易条件", conf = {
    })

    response = with_metaclass(ResponseFieldSet)
    response.total = ResponseField(IntField, desc = "数据总数")
    response.total_page = ResponseField(IntField, desc = "总页码数")
    response.data_list = ResponseField(ListField, desc = "用户列表", fmt = \
                                       DictField(desc = "用户详情", conf = {
                                            'id': IntField(desc = "交易ID"),
                                            'number': CharField(desc = "交易编号"),
                                            'amount': IntField(desc = "交易金额"),
                                            'pay_type': CharField(desc = "交易方式"),
                                            'remark': CharField(desc = "交易说明"),
                                            'create_time': DatetimeField(desc = "交易时间"),
                                        }))
    response.total = ResponseField(IntField, desc = "数据总数")
    response.total_page = ResponseField(IntField, desc = "总页码数")

    @classmethod
    def get_desc(cls):
        return "客户交易搜索接口"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        transaction_spliter = CustomerFinanceServer.search_transaction_record(
            current_page = request.current_page,
            **request.search_info,
        )
        return transaction_spliter

    def fill(self, response, transaction_spliter):
        data_list = [{
            'id': transaction.id,
            'number': transaction.number,
            'amount': transaction.amount,
            'pay_type': transaction.pay_type,
            'remark': transaction.remark,
            'create_time': transaction.create_time,
        } for transaction in transaction_spliter.data]
        response.data_list = data_list
        response.total = transaction_spliter.total
        response.total_page = transaction_spliter.total_page
        return response
