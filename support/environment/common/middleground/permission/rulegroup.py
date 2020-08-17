# coding=UTF-8

from support.common.maker import BaseLoader


class RuleGroupLoader(BaseLoader):

    def generate(self):
        return [
            {
                'name': '超级管理员权限',
                'description': "超级管理员权限",
            }
        ]
