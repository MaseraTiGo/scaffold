# coding=UTF-8

'''
Created on 2020年6月30日

@author: Roy
'''

from infrastructure.core.field.base import CharField, DictField, \
        IntField, ListField, BooleanField, MobileField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet

from agile.customer.manager.api import CustomerAuthorizedApi
from abs.middleground.business.person.manager import PersonServer


class Add(CustomerAuthorizedApi):

    request = with_metaclass(RequestFieldSet)
    request.is_default = RequestField(BooleanField, desc="是否默认地址")
    request.address_info = RequestField(DictField, desc="客户修改详情", conf={
        'contacts': CharField(desc="联系人"),
        'gender': CharField(desc="性别"),
        'phone': MobileField(desc="手机号"),
        'city': CharField(desc="城市"),
        'address': CharField(desc="详细地址"),
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "添加地址接口"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        customer = self.auth_user
        PersonServer.add_address(
            customer.person_id,
            request.is_default,
            **request.address_info
        )

    def fill(self, response):
        return response


class Get(CustomerAuthorizedApi):

    request = with_metaclass(RequestFieldSet)
    request.address_id = RequestField(IntField, desc="地址ID")

    response = with_metaclass(ResponseFieldSet)
    response.address_info = ResponseField(DictField, desc="地址详情", conf={
        'id': IntField(desc="地址ID"),
        'contacts': CharField(desc="联系人"),
        'gender': CharField(desc="性别"),
        'phone': CharField(desc="手机号"),
        'city': CharField(desc="城市"),
        'address': CharField(desc="详细地址"),
        'is_default': BooleanField(desc="是否是默认"),
    })

    @classmethod
    def get_desc(cls):
        return "获取地址详情"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        return PersonServer.get_address(request.address_id)

    def fill(self, response, address):
        response.address_info = {
            'id': address.id,
            'contacts': address.contacts,
            'gender': address.gender,
            'city': address.city,
            'phone': address.phone,
            'address': address.address,
            'is_default': address.is_default,
        }
        return response


class Update(CustomerAuthorizedApi):

    request = with_metaclass(RequestFieldSet)
    request.address_id = RequestField(IntField, desc="地址ID")
    request.is_default = RequestField(BooleanField, desc="是否默认地址")
    request.update_info = RequestField(DictField, desc="客户修改详情", conf={
        'contacts': CharField(desc="联系人", is_required=False),
        'gender': CharField(desc="性别", is_required=False),
        'phone': MobileField(desc="手机号", is_required=False),
        'city': CharField(desc="城市", is_required=False),
        'address': CharField(desc="详细地址", is_required=False),
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "客户地址修改接口"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        PersonServer.update_address(
            request.address_id,
            request.is_default,
            **request.update_info
        )

    def fill(self, response):
        return response


class All(CustomerAuthorizedApi):

    request = with_metaclass(RequestFieldSet)

    response = with_metaclass(ResponseFieldSet)
    response.address_list = ResponseField(
        ListField,
        desc="地址列表",
        fmt=DictField(
            desc="地址详情",
            conf={
                    'id': IntField(desc="地址ID"),
                    'contacts': CharField(desc="联系人"),
                    'gender': CharField(desc="性别"),
                    'phone': CharField(desc="手机号"),
                    'city': CharField(desc="城市"),
                    'address': CharField(desc="详细地址"),
                    'is_default': BooleanField(desc="是否是默认"),
            }))

    @classmethod
    def get_desc(cls):
        return "客户地址列表"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        address_sort_list = []
        customer = self.auth_user
        address_list = list(PersonServer.get_all_address(customer.person_id))
        for address in address_list:
            if address.is_default:
                address_sort_list.append(address)
                address_list.remove(address)
        address_sort_list.extend(address_list)
        return address_sort_list

    def fill(self, response, address_qs):
        response.address_list = [{
            'id': address.id,
            'contacts': address.contacts,
            'gender': address.gender,
            'city': address.city,
            'phone': address.phone,
            'address': address.address,
            'is_default': address.is_default,
        } for address in address_qs]
        return response


class Remove(CustomerAuthorizedApi):

    request = with_metaclass(RequestFieldSet)
    request.address_id = RequestField(IntField, desc="地址ID")

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "删除地址信息"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        PersonServer.remove_address(request.address_id)

    def fill(self, response):
        return response
