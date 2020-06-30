# coding=UTF-8

from infrastructure.core.service.base import BaseAPIService


class CustomerMobileService(BaseAPIService):

    @classmethod
    def get_name(self):
        return "客户服务"

    @classmethod
    def get_desc(self):
        return "针对客户提供的相关的服务"

    @classmethod
    def get_flag(cls):
        return "customer-mobile"


customer_mobile_service = CustomerMobileService()
from agile.customer.apis.customer.account.vcode import Phone, Image
customer_mobile_service.add(Phone, Image)

from agile.customer.apis.customer.account import Login, Logout
customer_mobile_service.add(Login, Logout)

from agile.customer.apis.customer.myself import Get, Update
customer_mobile_service.add(Get, Update)
