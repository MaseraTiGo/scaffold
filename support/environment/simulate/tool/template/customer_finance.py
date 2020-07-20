# coding=UTF-8

import random
import json

from src.infrastructure.utils.common.timetools import get_sequence_date
from support.generator.field.normal import *
from support.generator.field.model import *
from support.simulate.tool.template.base import BaseTemplate


class CustomerBalanceTemplate(BaseTemplate):

    def generate(self):
        balance_list = []
        start_time = datetime.datetime(2019, 7, 1, 1, 23)
        end_time = datetime.datetime.today()
        for time in get_sequence_date(start_time, end_time):
            for _ in range(random.randint(0,5)):
                is_input = random.choice([False, True])
                amount = AmountHelper().generate()
                balance = {
                    'amount':  amount if is_input else 0 - amount,
                    'pay_type': PayTypeConstant().generate(),
                    'remark': "{} 客户充值 ".format(time),
                    'create_time': time,
                    'is_input': is_input
                }
                balance_list.append(balance)
        return balance_list
