# coding=UTF-8

from infrastructure.core.field.base import CharField, DictField, \
        IntField, ListField, DatetimeField, BooleanField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet

from agile.crm.manager.api import StaffAuthorizedApi
from abs.services.customer.personal.manager import CustomerServer


class Search(StaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.customer_id = RequestField(IntField, desc = "客户id")

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(
        ListField,
        desc = "地址列表",
        fmt = DictField(
            desc = "客户地址",
            conf = {
                'id': IntField(desc = "地址id"),
                'contacts': CharField(desc = "联系人"),
                'gender': CharField(desc = "性别"),
                'phone': CharField(desc = "联系电话"),
                'city': CharField(desc = "城市"),
                'address': CharField(desc = "详细地址"),
                'is_default': BooleanField(desc = "是否默认地址"),
                'create_time': DatetimeField(desc = "添加时间"),
            }
        )
    )

    @classmethod
    def get_desc(cls):
        return "搜索客户地址列表"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        address_list = CustomerServer.get_customer_address(
                 request.customer_id
               )
        return address_list

    def fill(self, response, address_list):
        data_list = [{
                'id': address.id,
                'contacts': address.contacts,
                'gender': address.gender,
                'phone': address.phone,
                'city': address.city,
                'address': address.address,
                'is_default': address.is_default,
                'create_time': address.create_time,
        } for address in address_list]
        response.data_list = data_list
        return response



