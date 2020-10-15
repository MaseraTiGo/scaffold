# coding=UTF-8

import json
from support.common.maker import BaseLoader


class ProductionLoader(BaseLoader):
    
    attribute_list = [{'attribute_list': [{'name': "普通"}, {'name': "VIP"}], 'category': "班级"}]
    workflow_list = [{"name": "test", "type": "test", "description": "test"}]

    def generate(self):
        return [
            {
                'name': '高起专',
                'brand_name': "成教",
                'description': '教育行业',
                'attribute_list': json.dumps(self.attribute_list),
                'workflow_list': json.dumps(self.workflow_list)
            },
            {
                'name': '高起专',
                'brand_name': "网教",
                'description': '教育行业',
                'attribute_list': json.dumps(self.attribute_list),
                'workflow_list': json.dumps(self.workflow_list)
            },
            {
                'name': '高升专',
                'brand_name': "成教",
                'description': '教育行业',
                'attribute_list': json.dumps(self.attribute_list),
                'workflow_list': json.dumps(self.workflow_list)
            },
            {
                'name': '专升本',
                'brand_name': "成教",
                'description': '教育行业',
                'attribute_list': json.dumps(self.attribute_list),
                'workflow_list': json.dumps(self.workflow_list)
            },
            {
                'name': '专升本',
                'brand_name': "自考",
                'description': '教育行业',
                'attribute_list': json.dumps(self.attribute_list),
                'workflow_list': json.dumps(self.workflow_list)
            },
        ]
