# coding=UTF-8

import json
from support.common.maker import BaseLoader


class ProductionLoader(BaseLoader):

    def generate(self):
        return [
            {
                'name': '专升本',
                'brand_name': "成教",
                'description': '教育行业',
                'attribute_list': json.dumps([
                    {
                        'category': "课程",
                        'attribute_list': [
                            {
                                'name': "普通课程",
                            },
                            {
                                'name': "vip课程",
                            },
                        ],
                    }
                ]),
                'workflow_list': json.dumps([
                    {
                        'name': "流程一",
                        'type': "report",
                        'description': "这是第一个流程",
                    },
                    {
                        'name': "流程二",
                        'type': "report",
                        'description': "这是第二个流程",
                    },
                    {
                        'name': "流程三",
                        'type': "report",
                        'description': "这是第三个流程",
                    },
                ])
            },
            {
                'name': '专套本',
                'description': '教育行业',
                'brand_name': "成教",
                'attribute_list': json.dumps([
                    {
                        'category': "课程",
                        'attribute_list': [
                            {
                                'name': "普通课程",
                            },
                            {
                                'name': "vip课程",
                            },
                        ],
                    }
                ]),
                'workflow_list': json.dumps([
                    {
                        'name': "流程一",
                        'type': "report",
                        'description': "这是第一个流程",
                    },
                    {
                        'name': "流程二",
                        'type': "report",
                        'description': "这是第二个流程",
                    },
                    {
                        'name': "流程三",
                        'type': "report",
                        'description': "这是第三个流程",
                    },
                ])
            },
            {
                'name': '苹果4s',
                'brand_name': "苹果",
                'description': '电商行业',
                'attribute_list': json.dumps([
                    {
                        'category': "颜色",
                        'attribute_list': [
                            {
                                'name': "红",
                            },
                            {
                                'name': "黄",
                            },
                            {
                                'name': "蓝",
                            },
                            {
                                'name': "绿",
                            },
                        ],
                    },
                    {
                        'category': "类型",
                        'attribute_list': [
                            {
                                'name': "三网通",
                            },
                            {
                                'name': "移动定制",
                            },
                            {
                                'name': "电信定制",
                            },
                            {
                                'name': "联通定制",
                            },
                        ],
                    }
                ]),
                'workflow_list': json.dumps([
                    {
                        'name': "流程一",
                        'type': "report",
                        'description': "这是第一个流程",
                    },
                    {
                        'name': "流程二",
                        'type': "report",
                        'description': "这是第二个流程",
                    },
                    {
                        'name': "流程三",
                        'type': "report",
                        'description': "这是第三个流程",
                    },
                ])
            },
        ]
