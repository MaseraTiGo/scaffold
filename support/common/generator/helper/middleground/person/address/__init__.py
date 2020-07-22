# coding=UTF-8


from infrastructure.log.base import logger
from support.common.generator.base import BaseGenerator
from support.common.generator.helper import PersonGenerator
from abs.middleground.business.person.store import Address


class AddressGenerator(BaseGenerator):

    def __init__(self, address_infos):
        super(AddressGenerator, self).__init__()
        self._address_infos = self.init(address_infos)

    def get_create_list(self, result_mapping):
        person_list = result_mapping.get(PersonGenerator.get_key())
        address_list = []
        for person in person_list:
            for address_info in self._address_infos:
                address_info.update({
                    'person': person
                })
                address_list.append(address_info)
        return address_list

    def create(self, customer_info, result_mapping):
        address = Address.create(**customer_info)
        return address

    def delete(self):
        logger.info('================> delete customer <==================')
        return None