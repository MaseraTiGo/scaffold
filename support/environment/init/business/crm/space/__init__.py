# coding=UTF-8

import datetime
from support.common.maker import BaseLoader


class SpaceLoader(BaseLoader):

    def generate(self):
        return [
                {
                    'label': 'index_banner',
                    'name': '首页_上',
                    'width': 690,
                    'height': 360,
                },
                {
                    'label': 'index_mid',
                    'name': '首页_中',
                    'width': 690,
                    'height': 130,
                },
                {
                    'label': 'school_list',
                    'name': '院校列表_上',
                    'width': 690,
                    'height': 130,
                },
                {
                    'label': 'major_list',
                    'name': '专业列表_上',
                    'width': 690,
                    'height': 130,
                },
        ]
