# coding=UTF-8

from infrastructure.core.field.base import CharField,DictField,\
        IntField,ListField,DatetimeField,BooleanField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField,RequestFieldSet
from infrastructure.core.api.response import ResponseField,ResponseFieldSet

from agile.crm.manager.api import StaffAuthorizedApi
from abs.services.customer.personal.manager import CustomerServer
from abs.middleground.business.transaction.manager import TransactionServer


class Search(StaffAuthorizedApi):

    request=with_metaclass(RequestFieldSet)
    request.current_page=RequestField(IntField,desc="当前页码")
    request.customer_id=RequestField(IntField,desc="客户id")

    response=with_metaclass(ResponseFieldSet)
    response.total=ResponseField(IntField,desc="数据总数")
    response.total_page=ResponseField(IntField,desc="总页码数")
    response.data_list=ResponseField(
        ListField,
        desc="用户列表",
        fmt=DictField(
            desc="用户详情",
            conf={
                'id': IntField(desc="交易ID"),
                'number': CharField(desc="交易编号"),
                'amount': IntField(desc="交易金额"),
                'pay_type': CharField(desc="交易方式"),
                'business_type': CharField(desc="业务来源"),
                'remark': CharField(desc="交易说明"),
                'create_time': DatetimeField(desc="交易时间"),
            }
        )
    )
    response.total=ResponseField(IntField,desc="数据总数")
    response.total_page=ResponseField(IntField,desc="总页码数")

    @classmethod
    def get_desc(cls):
        return "搜索客户账户列表"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self,request):
        customer=CustomerServer.get(request.customer_id)
        transaction_spliter=TransactionServer.search_person_transaction(
            current_page=request.current_page,
            person_id=customer.person_id
        )
        return transaction_spliter

    def fill(self,response,transaction_spliter):
        data_list=[{
            'id': transaction.id,
            'number': transaction.number,
            'amount': transaction.amount,
            'pay_type': transaction.pay_type,
            'business_type': transaction.business_type,
            'remark': transaction.remark,
            'create_time': transaction.create_time,
        } for transaction in transaction_spliter.data]
        response.data_list=data_list
        response.total=transaction_spliter.total
        response.total_page=transaction_spliter.total_page
        return response