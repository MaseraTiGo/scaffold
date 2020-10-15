# coding=UTF-8

import random
from support.common.maker import BaseLoader


class ContactLoader(BaseLoader):

    def generate(self):
        return [
            {
                'contacts': '尚先生',
                'phone': '18888888888',
                'email': 'superman@qq.com',
                'gender': random.choice(['man', 'woman', 'unknown']),
            }
        ]
