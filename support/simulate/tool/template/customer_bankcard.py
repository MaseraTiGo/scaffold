# coding=UTF-8

import random
import json

from support.generator.field.normal import *
from support.generator.field.model import *
from support.simulate.tool.template.base import BaseTemplate


class CustomerBankcardTemplate(BaseTemplate):

    def generate(self):
        times = random.randint(3, 10)
        bankcard_list = []
        for _ in range(times):
            bank_name, bank_code, bank_number = BankCardHelper().generate()
            bankcard = {
                'bank_number': NameHelper().generate(),
                'bank_name': NameHelper().generate(),
                'bank_code': NameHelper().generate(),
                'phone': PhoneHelper().generate(),
                'name': NameHelper().generate(),
                'identification': IdentificationHelper().generate(),
            }
            bankcard_list.append(bankcard)
        return bankcard_list
