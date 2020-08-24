# coding=UTF-8

import json
from support.common.maker import BaseLoader


class ProductionLoader(BaseLoader):

    def generate(self):
        return [
            {
                'name': '高起专',
                'brand_name': "成教",
                'description': '教育行业',
                'attribute_list': json.dumps([]),
                'workflow_list': json.dumps([])
            },
            {
                'name': '高起专',
                'brand_name': "成教",
                'description': '教育行业',
                'attribute_list': json.dumps([]),
                'workflow_list': json.dumps([])
            },
            {
                'name': '高升专',
                'brand_name': "成教",
                'description': '教育行业',
                'attribute_list': json.dumps([]),
                'workflow_list': json.dumps([])
            },
            {
                'name': '专升本',
                'brand_name': "成教",
                'description': '教育行业',
                'attribute_list': json.dumps([]),
                'workflow_list': json.dumps([])
            },
            {
                'name': '专升本',
                'brand_name': "自考",
                'description': '教育行业',
                'attribute_list': json.dumps([]),
                'workflow_list': json.dumps([])
            },
        ]
