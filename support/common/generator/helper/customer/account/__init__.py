# coding=UTF-8

import hashlib
from infrastructure.utils.common.dictwrapper import DictWrapper
from support.common.generator.base import BaseGenerator
from support.common.generator.helper import CustomerGenerator

from abs.middleground.business.account.utils.constant import StatusTypes
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
                "customer_id": customer.id
            })
            account_list.append(account_info)
        return account_list

    def create(self, account_info, result_mapping):
        account_qs = CustomerAccount.query().filter(
            customer_id=account_info.customer_id
        )
        if account_qs.count():
            account = account_qs[0]
        else:
            account = CustomerAccount.create(**account_info)
        return account

    def delete(self):
        print('==================>>> delete account <======================')
        return None
