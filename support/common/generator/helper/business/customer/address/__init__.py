# coding=UTF-8


from infrastructure.log.base import logger
from support.generator.base import BaseGenerator
from model.common.model_user_base import UserCertification
from support.generator.helper import CustomerGenerator
from model.store.model_customer import CustomerAddress


class CustomerAddressGenerator(BaseGenerator):

    def __init__(self, address_infos):
        super(CustomerAddressGenerator, self).__init__()
        self._address_infos = self.init(address_infos)

    def get_create_list(self, result_mapping):
        customer_list = result_mapping.get(CustomerGenerator.get_key())
        address_list = []
        for customer in customer_list:
            for address_info in self._address_infos:
                address_info.update({
                    'customer': customer
                })
                address_list.append(address_info)
        return address_list

    def create(self, customer_info, result_mapping):
        address = CustomerAddress.create(**customer_info)
        return address

    def delete(self):
        print('======================>>> delete customer <======================')
        return None
