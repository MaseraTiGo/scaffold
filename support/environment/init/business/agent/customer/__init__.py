# coding=UTF-8

import random
from support.common.maker import BaseLoader


class CustomerLoader(BaseLoader):

    def generate(self):
        return [
            {
                'contacts': '六先生',
                'name': '六先生',
                'phone': '16666666666',
                'email': 'sixsixsix@six.com',
                'education': 'doctor',
                'gender': random.choice(['man', 'woman', 'unknown']),
            }
        ]
