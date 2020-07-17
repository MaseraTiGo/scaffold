# coding=UTF-8

import datetime
from support.generator.field.model.constant import GenderConstant
from support.init.base import BaseLoader


class StaffLoader(BaseLoader):

    def load(self):
        return [{
            'name': 'admin',
            'nick': 'admin',
            'gender': GenderConstant().generate(),
            'birthday': datetime.datetime(2018, 6, 1),
            'work_number': 'BQ10001',
            'phone': '15527703115',
            'email': '237818280@qq.com',
            'is_admin': True,
            'remark': '这是系统管理员'
        }]
