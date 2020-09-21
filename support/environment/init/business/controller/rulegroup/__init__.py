# coding=UTF-8


import json
from support.common.maker import BaseLoader


class RuleGroupLoader(BaseLoader):

    def generate(self):
        return [
            {
                'name': '管理员',
                'describe': "超级角色",
                'organization': "公司",
                "platform": "中台",
                'company': "橙鹿教育科技（湖北）有限公司",
                'content': json.dumps([
                    '授权管理-权限授权-查询',
                    '授权管理-权限授权-添加',
                    '授权管理-权限授权-删除',
                    '权限管理-权限组管理-查询',
                    '权限管理-权限组管理-删除',
                    '权限管理-权限组管理-添加',
                    '权限管理-权限组管理-修改',
                ])
            },
            {
                'name': '人事管理员',
                'describe': "超级角色",
                'organization': "公司",
                "platform": "中台",
                'company': "橙鹿教育科技（湖北）有限公司",
                'content': json.dumps([
                    '权限管理-职位管理-查询',
                    '权限管理-职位管理-添加',
                    '权限管理-职位管理-删除',
                    '权限管理-部门管理-查询',
                    '权限管理-部门管理-删除',
                    '权限管理-部门管理-添加',
                    '权限管理-部门管理-修改',
                    '权限管理-员工列表-查询',
                    '权限管理-员工列表-添加',
                    '权限管理-员工列表-修改',
                ])
            },
        ]
