# coding=UTF-8

import datetime
from support.generator.field.model.constant import GenderConstant
from support.init.base import BaseLoader


class CustomerLoader(BaseLoader):

    def load(self):
        return [{
            'nick': '小清新',
            'name': '测试账户',
            'gender': GenderConstant().generate(),
            'birthday': datetime.datetime(2018, 6, 1),
            'phone': '15527703115',
            'email': '237818280@qq.com',
            'wechat': 'test_128481282_x',
            'qq': '237818280',
        }]
