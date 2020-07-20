# coding=UTF-8

import random
import datetime

from infrastructure.utils.common.timetools import get_sequence_date
from support.common.generator.field.normal import AmountHelper
from support.common.generator.field.model import PayTypeConstant
from support.common.maker import BaseLoader


class CustomerBalanceLoader(BaseLoader):

    def generate(self):
        balance_list = []
        start_time = datetime.datetime(2019, 11, 1, 1, 23)
        end_time = datetime.datetime.today()
        for time in get_sequence_date(start_time, end_time):
            for _ in range(random.randint(0, 5)):
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
