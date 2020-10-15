# coding=UTF-8

from random import choice

from support.common.maker import BaseLoader


class AgentStaffLoader(BaseLoader):

    def generate(self):
        return [{
            'name': 'IronMan',
            'phone': '13237161434',
            'permission_id': 2,
            'is_admin': True,
            'work_number': 'BQ11111111'
        },
            {
                'name': 'Thor',
                'phone': '13237161435',
                'permission_id': 2,
                'is_admin': choice([True, False]),
                'work_number': 'BQ11111112'
            },
            {
                'name': 'Hulk',
                'phone': '13237161436',
                'permission_id': 2,
                'is_admin': choice([True, False]),
                'work_number': 'BQ11111113'
            },

        ]
