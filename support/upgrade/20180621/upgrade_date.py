# coding=UTF-8

from support.upgrade.base import BaseUpgrade
from model.models import Rule


class RuleUpgrad(BaseUpgrade):

    def _get_test_data(self):
        data_list = [
                    {
                        "name": "权限管理",
                        "mark": "permise_mod",
                        "parent_id": 0,
                        "apis": "",
                        "describe": "权限管理模块",
                        "children": [
                                         {
                                            "name": "员工列表",
                                            "mark": "staff_page",
                                            "apis": "user.staff.list",
                                            "describe": "员工列表页面",
                                            "children": [
                                                              {
                                                                    "name": "编辑",
                                                                    "mark": "get_fun",
                                                                    "apis": "user.staff.getbyadmin",
                                                                    "describe": "编辑员工详情"
                                                               },
                                                               {
                                                                    "name": "编辑保存",
                                                                    "mark": "update_fun",
                                                                    "apis": "user.staff.updatebyadmin",
                                                                    "describe": "编辑保存员工详情"
                                                               },
                                                               {
                                                                    "name": "添加",
                                                                    "mark": "add_fun",
                                                                    "apis": "account.staff.add",
                                                                    "describe": "添加员工"
                                                               }   
                                                        ]
                                          },
                                          {
                                            "name": "角色列表",
                                            "mark": "role_page",
                                            "apis": "permise.staff.role.list",
                                            "describe": "角色列表页面",
                                            "children": [
                                                              {
                                                                    "name": "添加角色",
                                                                    "mark": "add_fun",
                                                                    "apis": "permise.staff.role.add",
                                                                    "describe": "添加角色"
                                                               },
                                                               {
                                                                    "name": "编辑角色",
                                                                    "mark": "get_fun",
                                                                    "apis": "permise.staff.role.get",
                                                                    "describe": "编辑角色"
                                                               },
                                                               {
                                                                    "name": "编辑保存角色",
                                                                    "mark": "update_fun",
                                                                    "apis": "permise.staff.role.update",
                                                                    "describe": "编辑保存角色"
                                                               }, 
                                                               {
                                                                    "name": "删除角色",
                                                                    "mark": "remove_fun",
                                                                    "apis": "permise.staff.role.remove",
                                                                    "describe": "删除角色"
                                                               }, 
                                                        ]
                                          },
                                          {
                                            "name": "部门列表",
                                            "mark": "department_page",
                                            "apis": "permise.staff.department.list",
                                            "describe": "部门列表页面",
                                            "children": [
                                                              {
                                                                    "name": "添加部门",
                                                                    "mark": "add_fun",
                                                                    "apis": "permise.staff.department.add",
                                                                    "describe": "添加部门"
                                                               },
                                                               {
                                                                    "name": "编辑部门",
                                                                    "mark": "get_fun",
                                                                    "apis": "permise.staff.department.get",
                                                                    "describe": "编辑部门"
                                                               },
                                                               {
                                                                    "name": "编辑保存部门",
                                                                    "mark": "update_fun",
                                                                    "apis": "permise.staff.department.update",
                                                                    "describe": "编辑保存部门"
                                                               }, 
                                                               {
                                                                    "name": "删除部门",
                                                                    "mark": "remove_fun",
                                                                    "apis": "permise.staff.department.remove",
                                                                    "describe": "删除部门"
                                                               }, 
                                                        ]
                                          },
                                     ]
                    }
               ]
        return data_list

    def run(self):
        def _register_children(rule, children_list):
            for cru in children_list:
                child_rule = Rule.create(name = cru["name"], mark = cru["mark"], parent_id = rule.id, \
                                         apis = cru["apis"], describe = cru["describe"])
                if "children" in cru:
                    _register_children(child_rule, cru["children"])

        data_list = self._get_test_data()
        for ru in data_list:
            rule = Rule.create(name = ru["name"], mark = ru["mark"], parent_id = ru["parent_id"], \
                               apis = ru["apis"], describe = ru["describe"])
            if "children" in ru:
                _register_children(rule, ru["children"])
