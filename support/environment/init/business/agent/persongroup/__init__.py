# coding=UTF-8


import json
from support.common.maker import BaseLoader


class PersonGroupLoader(BaseLoader):

    def generate(self):
        return [
            {
                'name': '超级管理员',
                'describe': "超级角色",
                'remark': 'nothing',
                'company_name': '尚德教育'
            },
        ]
