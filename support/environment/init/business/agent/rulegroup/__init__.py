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
                "platform": "尚德教育",
                'company': "尚德教育",
                'content': json.dumps([
                    '所有权限-组织结构-权限组管理-查询',
                    '所有权限-组织结构-权限组管理-添加',
                    '所有权限-组织结构-权限组管理-删除',
                    '所有权限-组织结构-权限组管理-修改',
                    '所有权限-组织结构-职位管理-查询',
                    '所有权限-组织结构-职位管理-删除',
                    '所有权限-组织结构-职位管理-添加',
                    '所有权限-组织结构-职位管理-修改',
                    '所有权限-组织结构-部门管理-查询',
                    '所有权限-组织结构-部门管理-删除',
                    '所有权限-组织结构-部门管理-添加',
                    '所有权限-组织结构-部门管理-修改',
                    '所有权限-组织结构-员工列表-查询',
                    '所有权限-组织结构-员工列表-添加',
                    '所有权限-组织结构-员工列表-修改',
                    '所有权限-组织结构-员工列表-修改账号',
                    '所有权限-组织结构-员工列表-修改部门',

                    '所有权限-客户管理-客户列表-查询',
                    '所有权限-客户管理-客户列表-详情',

                    '所有权限-商品管理-商品列表-查询',
                    '所有权限-商品管理-商品列表-详情',
                    '所有权限-商品管理-商品审核-查询',
                    '所有权限-商品管理-商品审核-详情',
                    '所有权限-商品管理-商品审核-添加规格',
                    '所有权限-商品管理-商品审核-提交审核',

                    '所有权限-订单管理-订单列表-查询',
                    '所有权限-订单管理-订单列表-详情',
                    '所有权限-订单管理-合同列表-查询',

                    '所有权限-订单管理-合同模板-查询',
                    '所有权限-订单管理-合同模板-预览',
                    '所有权限-订单管理-合同模板-删除',
                    '所有权限-订单管理-合同模板-添加',
                    '所有权限-订单管理-合同模板-修改',

                    '所有权限-工作台-我的客户-查询',
                    '所有权限-工作台-我的客户-添加',
                    '所有权限-工作台-我的客户-修改',
                ])
            },
            {
                'name': '人事管理员',
                'describe': "超级角色",
                'organization': "公司",
                "platform": "尚德教育",
                'company': "尚德教育",
                'content': json.dumps([
                    '所有权限-组织结构-权限组管理-查询',
                    '所有权限-组织结构-权限组管理-添加',
                    '所有权限-组织结构-权限组管理-删除',
                    '所有权限-组织结构-权限组管理-修改',
                    '所有权限-组织结构-职位管理-查询',
                    '所有权限-组织结构-职位管理-删除',
                    '所有权限-组织结构-职位管理-添加',
                    '所有权限-组织结构-职位管理-修改',
                    '所有权限-组织结构-部门管理-查询',
                    '所有权限-组织结构-部门管理-删除',
                    '所有权限-组织结构-部门管理-添加',
                    '所有权限-组织结构-部门管理-修改',
                    '所有权限-组织结构-员工列表-查询',
                    '所有权限-组织结构-员工列表-添加',
                    '所有权限-组织结构-员工列表-修改',
                ])
            },
        ]