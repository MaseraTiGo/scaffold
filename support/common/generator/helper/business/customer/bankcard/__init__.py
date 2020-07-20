# coding=UTF-8


from infrastructure.log.base import logger
from support.generator.base import BaseGenerator
from model.common.model_user_base import UserCertification
from support.generator.helper import CustomerGenerator
from model.store.model_customer import CustomerBankCard


class CustomerBankcardGenerator(BaseGenerator):

    def __init__(self, bankcard_infos):
        super(CustomerBankcardGenerator, self).__init__()
        self._bankcard_infos = self.init(bankcard_infos)

    def get_create_list(self, result_mapping):
        customer_list = result_mapping.get(CustomerGenerator.get_key())
        bankcard_list = []
        for customer in customer_list:
            for bankcard_info in self._bankcard_infos:
                bankcard_info.update({
                    'customer': customer
                })
                bankcard_list.append(bankcard_info)
        return bankcard_list

    def create(self, customer_info, result_mapping):
        bankcard = CustomerBankCard.create(**customer_info)
        return bankcard

    def delete(self):
        print('======================>>> delete customer <======================')
        return None
