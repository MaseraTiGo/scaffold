# coding=UTF-8


from support.common.maker import BaseLoader


class PositionLoader(BaseLoader):

    def generate(self):
        return [
            {
                'name': '总经理',
                'parent': "",
                'describe': "总经理",
                'rule_group': "管理员",
                'remark': "",
                "platform": "橙鹿教育代理商平台",
                'company': "橙鹿教育科技（湖北）有限公司",
            },
            {
                'name': '人事总监',
                'parent': "总经理",
                'describe': "人事总监",
                'rule_group': "人事管理员",
                'remark': "",
                "platform": "橙鹿教育代理商平台",
                'company': "橙鹿教育科技（湖北）有限公司",
            },
            {
                'name': '系统管理员',
                'parent': "总经理",
                'describe': "系统管理员",
                'rule_group': "管理员",
                'remark': "",
                "platform": "橙鹿教育代理商平台",
                'company': "橙鹿教育科技（湖北）有限公司",
            }
        ]
