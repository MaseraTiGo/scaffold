# coding=UTF-8

import random
import json

from support.generator.field.normal import *
from support.generator.field.model import *
from support.simulate.tool.template.base import BaseTemplate


class CustomerAddressTemplate(BaseTemplate):

    def generate(self):
        birthday  = DateHelper().generate(years = 30)
        phone = PhoneHelper().generate()

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
