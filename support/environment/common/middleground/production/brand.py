# coding=UTF-8

from support.common.maker import BaseLoader


class BrandLoader(BaseLoader):

    def generate(self):
        return [
            {
                'name': '成教',
                'industry': '教育',
                'description': '教育行业',
            },
            {
                'name': '网教',
                'industry': '教育',
                'description': '教育行业',

            },
            {
                'name': '苹果',
                'industry': '电商',
                'description': '电商行业',
            },
            {
                'name': '华为',
                'industry': '电商',
                'description': '电商行业',
            },
        ]