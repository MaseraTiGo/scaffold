# coding=UTF-8

import random
from support.common.maker import BaseLoader


class GoodsLoader(BaseLoader):

    def generate(self):
        return [
            {
                'template_id': 1,
            },
            {
                'template_id': 1,
            },
            {
                'template_id': 1,
            }
        ]
