# coding=UTF-8

import random
import json
from support.simulate.tool.base.general import *
from support.simulate.tool.base.model import EquipStatusHelper,\
        CustomerHelper, LogisticsItemHelper, ProductModelHelper
from support.simulate.tool.template.base import BaseTemplate


class EquipmentTemplate(BaseTemplate):

    def generate(self, is_pay = False, is_send = False):
        pm = ProductModelHelper().generate()
        return {
            'customer': None,
            'logisticsItem': None,
            'order': None,
            'product': pm.product,
            'product_model': pm,
            'code': EquipNumberHelper().generate(),
            'last_cal_time': DateTimeHelper().generate(),
            'total_amount': random.randint(0,99999999),
            'create_time': DateTimeHelper(years = 1).generate(),
        }
