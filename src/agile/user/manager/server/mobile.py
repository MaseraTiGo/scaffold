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
from agile.crm.apis.staff.account.vcode import Phone, Image
crm_pc_service.add(Phone, Image)
