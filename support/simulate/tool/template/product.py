# coding=UTF-8

import random
import json
from support.simulate.tool.base.general import *
from support.simulate.tool.base.model import GenderHelper, RoleHelper, DepartmentHelper
from support.simulate.tool.template.base import BaseTemplate


class ProductTemplate(BaseTemplate):

    def get_names(self):
        return ['蓝牙', '点刷', 'pos']

    def generate(self):
        name = random.choice(self.get_names())
        return {
            'name': name,
            'alias': name + 'alias',
            'introduction': name + '简介',
            'details': name + '详情',
            'thumbnail': json.dumps([]),
            'images': json.dumps([]),
            'postage': random.randint(0, 500),
            'create_time': DateTimeHelper().generate(years = 2)
        }


class ProductModelTemplate(BaseTemplate):

    max_len = 20
    min_len = 4

    def __init__(self, product_name):
        self._product_name = product_name

    def generate_model_name(self, product_name):
        return product_name + "_" + str(random.randint(0, 500))

    def generate_stock(self):
        return random.randint(0, 500)

    def generate_rate(self):
        return random.randint(0, 100)

    def generate(self):
        pm_list = []
        for _ in range(random.randint(self.min_len,self.max_len)):
            template = {
                'name': self.generate_model_name(self._product_name),
                'product_name': self._product_name,
                'rate': self.generate_rate(),
                'stock': self.generate_stock(),
                'create_time': DateTimeHelper().generate(years = 2)
            }
            pm_list.append(template)
        return pm_list


class ChannelTemplate(BaseTemplate):

    def generate_name(self):
        return random.choice(['京东', '一号店', '社群', '淘宝'])

    def generate(self):
        name = self.generate_name()
        return {
            'name': name,
            'single_point_money': random.randint(100, 9999),
            'single_repair_money': random.randint(100, 9999),
            'remark': name + '备注',
            'create_time': DateTimeHelper().generate(years = 2)
        }


class ShopTemplate(BaseTemplate):

    def __init__(self, channel_name):
        self._channel_name = channel_name

    def generate_name(self):
        return self._channel_name + "_" + str(random.randint(0, 5))

    def generate_channel_name(self):
        return random.choice([self._channel_name, ""])

    def generate(self):
        name = self.generate_name()
        channel_name = self.generate_channel_name()
        return {
            'channel_name': channel_name,
            'name': name,
            'single_point_money': random.randint(100, 9999),
            'single_repair_money': random.randint(100, 9999),
            'is_distribution': random.choice([True, False]),
            'remark': name + "备注",
            'create_time': DateTimeHelper().generate(years = 2)
        }


class GoodsTemplate(BaseTemplate):

    max_len = 20
    min_len = 4

    def __init__(self, product_name, shop_name):
        self._product_name = product_name
        self._shop_name = shop_name

    def generate_product_name(self):
        return self._product_name
        # return random.choice(self._product_names)

    def generate(self):
        goods_list = []
        for _ in range(random.randint(self.min_len,self.max_len)):
            product_name = self.generate_product_name()
            template = {
                'shop_name': self._shop_name,
                'product_name': product_name,
                'code': GoodsNumberHelper().generate(),
                'price': random.randint(100, 9999),
                'rate': random.randint(0, 100),
                'name': product_name + '-店铺直营-alias',
                'alias': product_name + '大蓝牙-店铺直营-alias',
                'introduction':product_name + '大蓝牙-店铺直营-简介',
                'details': product_name + '大蓝牙-店铺直营-详情',
                'thumbnail': json.dumps([]),
                'images': json.dumps([]),
                'postage': random.randint(100, 500),
                're_num': random.randint(1,10),
                'create_time': DateTimeHelper().generate(years = 2)
            }
            goods_list.append(template)
        return goods_list
