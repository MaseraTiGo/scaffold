# coding=UTF-8

'''
Created on 2020年7月3日

@author: Roy
'''

from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet
from infrastructure.core.field.base import DictField, IntField, ListField

from agile.customer.manager.api import CustomerAuthorizedApi
from abs.middleground.business.transaction.manager import TransactionServer


class Monthly(CustomerAuthorizedApi):

    request = with_metaclass(RequestFieldSet)

    response = with_metaclass(ResponseFieldSet)
    response.statistics_list = ResponseField(
        ListField,
        desc="用户列表",
        fmt=DictField(
            desc="用户详情",
            conf={
                'year': IntField(desc="年份"),
                'month': IntField(desc="月份"),
                'income': IntField(desc="总收入额"),
                'expense': IntField(desc="总花费额"),
            }
        )
    )

    @classmethod
    def get_desc(cls):
        return "客户交易按月统计接口"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        statistics_result = TransactionServer.statistics_person_bymonth(
            person_id=self.auth_user.person_id,
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
