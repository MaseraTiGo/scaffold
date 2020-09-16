# coding=UTF-8

import datetime
from support.common.generator.field.model.constant import GenderConstant
from support.common.maker import BaseLoader


class StaffLoader(BaseLoader):

    def generate(self):
        return [{
            'name': 'yanfav5',
            'nick': 'yanfav5',
            'gender': GenderConstant().generate(),
            'birthday': datetime.datetime(2018, 6, 1),
            'work_number': 'BQ10001',
            'phone': '15527703115',
            'email': '237818280@qq.com',
            "platform": "中台",
            'company': "橙鹿教育科技（湖北）有限公司",
            'position': "系统管理员",
            'organization': "数据部",
            'is_admin': True,
            'remark': '这是系统管理员'
        }]
