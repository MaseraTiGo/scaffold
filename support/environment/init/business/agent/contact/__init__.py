# coding=UTF-8

import random
from support.common.maker import BaseLoader


class ContactLoader(BaseLoader):

    def generate(self):
        return [
            {
                'contacts': 'Thanos',
                'account': '13237161434',
                'phone': '13237161434',
                'email': 'superman@qq.com',
                'gender': random.choice(['man', 'woman', 'unknown']),
            }
        ]
