# coding=UTF-8

from support.common.maker import BaseLoader


class OrganizationLoader(BaseLoader):

    def generate(self):
        return [
            {
                'name': '总经办',
                'parent': "",
                'describe': "公司",
                'remark': "",
                "platform": "中台",
                'company': "橙鹿教育科技（湖北）有限公司",
                'position_list': ["总经理"]
            },
            {
                'name': '人事部',
                'parent': "总经办",
                'describe': "公司",
                'remark': "",
                "platform": "中台",
                'company': "橙鹿教育科技（湖北）有限公司",
                'position_list': ["人事总监"]
            },
            {
                'name': '数据部',
                'parent': "总经办",
                'describe': "公司",
                'remark': "",
                "platform": "中台",
                'company': "橙鹿教育科技（湖北）有限公司",
                'position_list': ["系统管理员"]
            },
        ]
