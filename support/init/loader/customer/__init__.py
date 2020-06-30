# coding=UTF-8

import datetime
from model.models import GenderTypes
from support.init.base import BaseLoader


class CustomerLoader(BaseLoader):

    def load(self):
        return [{
            'identification': '152127198907070012',
            'name': '测试账户',
            'gender': GenderTypes.MAN,
            'birthday': datetime.datetime(2018, 6, 1),
            'education': 'doctor',
            'phone': '15527703115',
            'email': '237818280@qq.com',
            'wechat': 'test_128481282_x',
            'qq': '237818280',
        }]
