# coding=UTF-8

import random

from support.common.generator.field.normal import BankCardHelper,\
        IdentificationHelper, PhoneHelper, NameHelper
from support.common.maker import BaseLoader


class BankcardLoader(BaseLoader):

    def generate(self):
        times = random.randint(3, 10)
        bankcard_list = []
        for _ in range(times):
            bank_name, bank_code, bank_number = BankCardHelper().generate()
            bankcard = {
                'bank_number': bank_number,
                'bank_name': bank_name,
                'bank_code': bank_code,
                'phone': PhoneHelper().generate(),
                'name': NameHelper().generate(),
                'identification': IdentificationHelper().generate(),
            }
            bankcard_list.append(bankcard)
        return bankcard_list
