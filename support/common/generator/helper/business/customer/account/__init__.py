# coding=UTF-8

import hashlib
from infrastructure.utils.common.dictwrapper import DictWrapper
from support.common.generator.base import BaseGenerator
from support.common.generator.helper import CustomerGenerator

from abs.middleground.business.account.utils.constant import StatusTypes,\
        PlatformTypes
from abs.middleground.business.person.models import Person
from abs.services.customer.account.models import CustomerAccount


class CustomerAccountGenerator(BaseGenerator):

    def get_create_list(self, result_mapping):
        customer_list = result_mapping.get(CustomerGenerator.get_key())
        account_list = []
        for customer in customer_list:
            person = Person.get_byid(customer.person_id)
            username = person.phone
            account_info = DictWrapper({
                "username": username,
                "password": hashlib.md5("123456".encode('utf8')).hexdigest(),
                "status": StatusTypes.ENABLE,
                "role_type": PlatformTypes.CUSTOMER,
                "role_id": customer.id
            })
            account_list.append(account_info)
        return account_list

    def create(self, account_info, result_mapping):
        account = CustomerAccount.get_byrole(
            account_info.role_id
        )
        if account is None:
            account = CustomerAccount.create(**account_info)
        return account

    def delete(self):
        print('==================>>> delete account <======================')
        return None
