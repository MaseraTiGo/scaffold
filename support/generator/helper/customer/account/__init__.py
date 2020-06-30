# coding=UTF-8

import hashlib
from infrastructure.log.base import logger
from infrastructure.utils.common.dictwrapper import DictWrapper
from support.generator.base import BaseGenerator
from model.common.model_account_base import StatusTypes
from support.generator.helper import CustomerGenerator
from model.store.model_customer import CustomerAccount


class CustomerAccountGenerator(BaseGenerator):

    def get_create_list(self, result_mapping):
        customer_list = result_mapping.get(CustomerGenerator.get_key())
        account_list = []
        for customer in customer_list:
            username = customer.phone
            account_info = DictWrapper({
                "username": username,
                "password": hashlib.md5("123456".encode('utf8'))\
                                .hexdigest(),
                "status": StatusTypes.ENABLE,
                "customer": customer
            })
            account_list.append(account_info)
        return account_list

    def create(self, account_info, result_mapping):
        account_qs = CustomerAccount.query().filter(customer = account_info.customer)
        if account_qs.count():
            account = account_qs[0]
        else:
            account = CustomerAccount.create(**account_info)
        return account

    def delete(self):
        print('==================>>> delete account <======================')
        return None
