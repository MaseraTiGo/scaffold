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


class Monthly(CustomerAuthorizedApi):

    request = with_metaclass(RequestFieldSet)

    response = with_metaclass(ResponseFieldSet)
    response.statistics_list = ResponseField(ListField, desc = "用户列表", fmt = \
                                       DictField(desc = "用户详情", conf = {
                                            'year': IntField(desc = "年份"),
                                            'month': IntField(desc = "月份"),
                                            'income': IntField(desc = "总收入额"),
                                            'expense': CharField(desc = "总花费额"),
                                        }))

    @classmethod
    def get_desc(cls):
        return "客户交易按月统计接口"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        statistics_result = CustomerFinanceServer.statistics_customer_bymonth(
            customer_id = self.auth_user.id,
        )
        return statistics_result

    def fill(self, response, statistics_result):
        statistics_list = [{
            'year': statistics[0],
            'month': statistics[1],
            'income': statistics[2],
            'expense': statistics[3],
        } for statistics in statistics_result]
        response.statistics_list = statistics_list
        return response
