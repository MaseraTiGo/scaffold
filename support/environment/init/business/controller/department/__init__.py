# coding=UTF-8

from support.environment.init.base import BaseLoader


class DepartmentLoader(BaseLoader):

    def generate(self):
        return [
            {
                'name': '公司',
                'parent': "",
                'describe': "公司",
            },
        ]
