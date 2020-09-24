# coding=UTF-8

'''
Created on 2020年6月18日

@author: Roy
'''

from infrastructure.core.field.base import CharField, DictField, \
        IntField, ListField, BooleanField, MobileField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet

from agile.agent.manager.api import AgentStaffAuthorizedApi
from abs.services.agent.agent.manager import AgentStaffServer


class Get(AgentStaffAuthorizedApi):
    """
    获取个人中心详情
    """
    request = with_metaclass(RequestFieldSet)

    response = with_metaclass(ResponseFieldSet)
    response.staff_info = ResponseField(
        DictField,
        desc = "用户详情",
        conf = {
            'name': CharField(desc = "姓名"),
            'gender': CharField(desc = "性别"),
            'birthday': CharField(desc = "生日"),
            'phone': CharField(desc = "电话"),
            'email': CharField(desc = "邮箱"),
            'work_number': CharField(desc = "员工工号"),
            'wechat': CharField(desc = "微信"),
            'qq': CharField(desc = "QQ"),
            'is_admin': BooleanField(desc = "是否是管理员"),
            'organization': DictField(
                desc = "组织信息",
                conf = {
                    'id': IntField(desc = "部门Id"),
                    'name': CharField(desc = "部门名称"),
                }
            ),
            'position': DictField(
                desc = "职位信息",
                conf = {
                    'id': IntField(desc = "职位Id"),
                    'name': CharField(desc = "职位名称"),
                }
            ),
        }
    )

    @classmethod
    def get_desc(cls):
        return "员工个人中心详情接口"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        return AgentStaffServer.get(self.auth_user.id)

    def fill(self, response, staff):
        response.staff_info = {
            'name': staff.person.name,
            'work_number': staff.work_number,
            'gender': staff.person.gender,
            'birthday': staff.person.birthday,
            'phone': staff.person.phone,
            'email': staff.person.email,
            'wechat': staff.person.wechat,
            'qq': staff.person.qq,
            'is_admin': staff.is_admin,
            'organization': {
                'id': staff.organization.id,
                'name': staff.organization.name,
            } if staff.organization else {
                'id':-1,
                'name': "",
            },
            'position': {
                'id': staff.position.id,
                'name': staff.position.name,
            } if staff.position else {
                'id':-1,
                "name": "",
            },
        }
        return response


class Update(AgentStaffAuthorizedApi):
    """
    修改个人中心详情
    """
    request = with_metaclass(RequestFieldSet)
    request.myself_info = RequestField(
        DictField,
        desc = "员工修改详情",
        conf = {
            'nick': CharField(desc = "昵称"),
            'head_url': CharField(desc = "头像"),
            'name': CharField(desc = "姓名"),
            'gender': CharField(desc = "性别"),
            'birthday': CharField(desc = "生日"),
            'phone': MobileField(desc = "电话"),
            'email': CharField(desc = "邮箱"),
            'work_number': CharField(desc = "员工工号"),
            'is_admin': BooleanField(desc = "是否是管理员"),
        }
    )

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "员工个人中心修改接口"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        staff = self.auth_user
        AgentStaffServer.update(staff.id, **request.myself_info)

    def fill(self, response):
        return response
