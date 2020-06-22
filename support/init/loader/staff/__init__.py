# coding=UTF-8

import datetime
from model.models import GenderTypes
from support.init.base import BaseLoader


class StaffLoader(BaseLoader):

    def load(self):
        return [{
            'identification': '152127198907070011',
            'name': 'admin',
            'gender': GenderTypes.MAN,
            'birthday': datetime.datetime(2018, 6, 1),
            'id_number': 'BQ10001',
            'phone': '15527703115',
            'email': '237818280@qq.com',
            'entry_time': datetime.datetime(1949, 10, 1),
            'education': 'doctor',
            'is_admin': True,
            'remark': '这是系统管理员'
        }]
