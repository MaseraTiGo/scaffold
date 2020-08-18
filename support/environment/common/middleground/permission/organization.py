# coding=UTF-8

from support.common.maker import BaseLoader


class OrganizationLoader(BaseLoader):

    def generate(self):
        return [
            {
                'name': '公司',
                'parent': "",
                'describe': "公司",
            },
        ]
