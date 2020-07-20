# coding=UTF-8

import random

from support.common.generator.field.normal import \
        AddressHelper, PhoneHelper, NameHelper
from support.common.generator.field.model import GenderConstant
from support.common.maker import BaseLoader


class AddressLoader(BaseLoader):

    def generate(self):
        times = random.randint(3, 10)
        address_list = []
        for _ in range(times):
            city, address = AddressHelper().generate()
            address = {
                'contacts': NameHelper().generate(),
                'gender': GenderConstant().generate(),
                'is_default': random.choice([False, True]),
                'phone': PhoneHelper().generate(),
                'city': city,
                'address': address,
            }
            address_list.append(address)
        return address_list
