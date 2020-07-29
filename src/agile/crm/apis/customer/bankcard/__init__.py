# coding=UTF-8

from infrastructure.core.field.base import CharField,DictField,\
        IntField,ListField,DatetimeField,BooleanField,HideField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField,RequestFieldSet
from infrastructure.core.api.response import ResponseField,ResponseFieldSet

from agile.crm.manager.api import StaffAuthorizedApi
from abs.services.customer.personal.manager import CustomerServer


class Search(StaffAuthorizedApi):
    request=with_metaclass(RequestFieldSet)
    request.customer_id=RequestField(IntField,desc="客户id")

    response=with_metaclass(ResponseFieldSet)
    response.data_list=ResponseField(
        ListField,
        desc="银行卡列表",
        fmt=DictField(
            desc="银行卡详情",
            conf={
                'id': IntField(desc="银行卡id"),
                'bank_name': CharField(desc="银行名称"),
                'bank_code': CharField(desc="银行编码"),
                'bank_number': HideField(desc="银行卡号"),
                'name': CharField(desc="开户人姓名"),
                'phone': CharField(desc="开户人手机号"),
                'identification': HideField(desc="开户人身份证"),
                'create_time': DatetimeField(desc="添加时间"),
            }
        )
    )

    @classmethod
    def get_desc(cls):
        return "搜索客户银行卡"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self,request):
        bankcard_list=CustomerServer.get_customer_bankcard(
                 request.customer_id
               )
        return bankcard_list

    def fill(self,response,bankcard_list):
        data_list=[{
                'id': bankcard.id,
                'bank_name': bankcard.bank_name,
                'bank_code': bankcard.bank_code,
                'bank_number': bankcard.bank_number,
                'name': bankcard.name,
                'phone': bankcard.phone,
                'identification': bankcard.identification,
                'create_time': bankcard.create_time,
        } for bankcard in bankcard_list]
        response.data_list=data_list
        return response



