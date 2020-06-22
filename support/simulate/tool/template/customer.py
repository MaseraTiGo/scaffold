# coding=UTF-8

import random
import json
from support.simulate.tool.base.general import *
from support.simulate.tool.base.model import *
from support.simulate.tool.template.base import BaseTemplate


class CustomerTemplate(BaseTemplate):

    def generate(self):
        birthday  = DateHelper().generate(years = 30)
        create_time = DateTimeHelper().generate(years = 2)
        phone = PhoneHelper().generate()
        name = NameHelper().generate()
        mobilephone = MobilePhoneHelper().generate()

        return {
            'identity': IdentityHelper().generate(),
            'name': name,
            'gender': GenderHelper().generate(),
            'birthday': birthday ,
            'phone': phone,
            'email': EmailHelper().generate(),
            'city': CityHelper().generate(),
            'address': AddressHelper().generate(),
            'wechat': phone,
            'nick': name,
            'mobilephone': mobilephone,
            'create_time': create_time,
        }


class SaleChanceTemplate(BaseTemplate):

    def create(self):
        create_time = DateTimeHelper().generate(years = 2)
        end_time = DateTimeHelper().generate(is_direction = True, days = 30)
        goods = GoodsHelper().generate()

        return {
            'customer_name': "",
            'shop': goods.shop,
            'goods': goods,
            'staff': StaffHelper().generate(),
            'order_count': 0,
            'order_ids': json.dumps([]),
            'remark': "机会备注",
            'end_time': end_time,
            'create_time': create_time,
        }

    def generate(self):
        return [self.create() for _ in range(random.randint(1,5))]


class OrderTemplate(BaseTemplate):

    def create(self):
        create_time = DateTimeHelper().generate(years = 2)

        return {
            'shop': ShopHelper().generate(),
            'customer_name': "",
            'order_sn': OrderNumberHelper().generate(),
            'paytype': PayTypesHelper().generate(),
            'pay_time': create_time,
            'status': "",
            'transaction_id': ThirdPayIDHelper().generate(),
            'consignee': NameHelper().generate(),
            'city': CityHelper().generate(),
            'address': AddressHelper().generate(),
            'phone': PhoneHelper().generate(),
            'messages': "送货需要快",
            'total_price': 0,
            'total_quantity': 0,
            'create_time': create_time,
        }

    def generate(self):
        return [self.create() for _ in range(random.randint(1,2))]


class OrderItemTemplate(BaseTemplate):

    def create(self):
        create_time = DateTimeHelper().generate(years = 2)
        goods = GoodsHelper().generate()

        return {
            'order_code': "",
            'goods': goods,
            'name': goods.name,
            'alias': goods.alias,
            'code': goods.code,
            'price': goods.price,
            'rate': goods.rate,
            'introduction': goods.introduction,
            'thumbnail': goods.thumbnail,
            'postage': goods.postage,
            'quantity': random.randint(1,5),
            'create_time': create_time,
        }

    def generate(self):
        return [self.create() for _ in range(random.randint(1,10))]


class ServiceTemplate(BaseTemplate):

    def generate(self):
        staff = StaffHelper().generate()
        return {
            'server': staff,
            'seller': "",
            'customer': "",
            'order': "",
            'end_time': "",
            'remark': "",
        }


class ServiceItemTmeplate(BaseTemplate):

    def generate(self):
        return {
            'customer': "",
            'service': "",
            'equipment': "",
            'buyinfo_status': EquipStatusHelper().generate(),
            'dsinfo_status': EquipStatusHelper().generate(),
            'rebate_status': EquipStatusHelper().generate(),
            'sn_status': EquipStatusHelper().generate(),
        }
