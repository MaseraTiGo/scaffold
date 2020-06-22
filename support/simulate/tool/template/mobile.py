# coding=UTF-8

import random
import json
from support.simulate.tool.base.general import *
from support.simulate.tool.base.model import StaffHelper
from support.simulate.tool.template.base import BaseTemplate


class MobileDevicesTemplate(BaseTemplate):

    def generate_brand(self):
        return random.choice([
            "小米",
            "魅族",
            "苹果",
        ])

    def generate_model(self):
        return random.choice([
            "红米",
            "魅蓝",
            "iphoneX",
        ])

    def generate_mobile_devices_status(self):
        return random.choice([
            "normal",
            "scrap",
            "idle",
            "other",
        ])

    def generate(self):
        staff = StaffHelper().generate(has_none = True)
        data = {
            'code': MobilePhoneHelper().generate(),
            'brand': self.generate_brand(),
            'model': self.generate_model(),
            'price': random.randint(10, 150) * 100,
            'status': self.generate_mobile_devices_status(),
            'remark': "备注"
        }

        return data


class MobilePhoneTemplate(BaseTemplate):

    def generate_operrator(self):
        return random.choice([
            "电信",
            "移动",
            "联通",
        ])

    def generate_tags(self):
        return random.choice([
            "30元套餐",
            "50元套餐",
            "80元套餐",
        ])

    def generate_mobile_status(self):
        return random.choice([
            "normal",
            "frozen",
            "seal",
            "arrears",
            "discontinuation",
            "other",
        ])

    def generate(self):
        staff = StaffHelper().generate(has_none = True)
        data = {
            'staff': staff,
            'operator': self.generate_operrator(),
            'rent': random.randint(10, 150) * 100,
            'tag': self.generate_tags(),
            'status': self.generate_mobile_status(),
            'create_time': DateTimeHelper().generate(years = 2),
            'remark': "备注"
        }

        if staff is not None:
            data.update({
                'name': staff.name,
                'identity': staff.identity,
                'phone_number': staff.phone,
            })
        else:
            data.update({
                'name': NameHelper().generate(),
                'identity': IdentityHelper().generate(),
                'phone_number': PhoneHelper().generate(),
            })

        return data


class MobileMaintainTemplate(BaseTemplate):

    def generate(self):
        data = {
            'staff': StaffHelper().generate(),
            'remark': "备注"
        }

        return data
