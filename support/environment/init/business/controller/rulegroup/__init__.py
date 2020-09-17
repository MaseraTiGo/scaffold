# coding=UTF-8


import json
from support.common.maker import BaseLoader


class RuleGroupLoader(BaseLoader):

    def generate(self):
        return [
            {
                'name': '超级管理员',
                'parent': "",
                'describe': "超级角色",
                'organization': "公司",
            }
        ]