# coding=UTF-8

'''
Created on 2020年6月18日

@author: Roy
'''

from infrastructure.core.field.base import CharField, DictField,\
        IntField, BooleanField, MobileField, DatetimeField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet

from agile.controller.manager.api import StaffAuthorizedApi
from abs.middleground.business.account.utils.constant import StatusTypes
from abs.middleground.business.person.utils.constant import GenderTypes
from abs.middleground.business.enterprise.manager import EnterpriseServer
from abs.middleground.technology.permission.manager import PermissionServer
from abs.services.controller.staff.manager import StaffServer
from abs.services.controller.account.manager import StaffAccountServer


class Get(StaffAuthorizedApi):
    """
    获取个人中心详情
    """
    request = with_metaclass(RequestFieldSet)
    request.appkey = RequestField(CharField, desc="appkey")

    response = with_metaclass(ResponseFieldSet)
    response.staff_info = ResponseField(
        DictField,
        desc="用户详情",
        conf={
            'id': IntField(desc="员工编号"),
            'name': CharField(desc="姓名"),
            'gender': CharField(desc="性别"),
            'birthday': CharField(desc="生日"),
            'wechat': CharField(desc="微信"),
            'qq': CharField(desc="QQ"),
            'phone': CharField(desc="电话"),
            'email': CharField(desc="邮箱"),
            'work_number': CharField(desc="员工工号"),
            'is_admin': BooleanField(desc="是否是管理员"),
            'organization': DictField(
                desc="组织信息",
                conf={
                    'id': IntField(desc="部门Id"),
                    'name': CharField(desc="部门名称"),
                }
            ),
            'position': DictField(
                desc="职位信息",
                conf={
                    'id': IntField(desc="职位Id"),
                    'name': CharField(desc="职位名称"),
                }
            ),
            'permission': CharField(
                desc="功能权限",
            ),
            'account_info': DictField(
                desc="账号信息",
                conf={
                    'nick': CharField(desc="昵称"),
                    'username': CharField(desc="账号"),
                    'head_url': CharField(desc="头像"),
                    'last_login_time': DatetimeField(desc="最后登录时间"),
                    'last_login_ip': CharField(desc="最后登录ip"),
                    'register_ip': CharField(desc="注册ip"),
                    'status': CharField(
                        desc="状态",
                        is_required=False,
                        choices=StatusTypes.CHOICES
                    ),
                    'update_time': DatetimeField(desc="更新时间"),
                    'create_time': DatetimeField(desc="创建时间"),
                }
            ),
            'company_info': DictField(
                desc="账号信息",
                conf={
                    'id': IntField(desc="id"),
                    'name': CharField(desc="昵称"),
                    'license_number': CharField(desc="营业执照"),
                    'create_time': DatetimeField(desc="创建时间"),
                }
            )
        }
    )

    @classmethod
    def get_desc(cls):
        return "员工个人中心详情接口"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        staff_id = self.auth_user.id
        staff = StaffServer.get(staff_id)
        staff.account = StaffAccountServer.get(staff_id)
        staff.company = EnterpriseServer.get(staff.company_id)
        staff.permission = PermissionServer.get_permission(
            request.appkey,
            staff.id,
            staff.is_admin
        )
        return staff

    def fill(self, response, staff):
        response.staff_info = {
            'id': staff.id,
            'name': staff.person.name,
            'work_number': staff.work_number,
            'gender': staff.person.gender,
            'birthday': staff.person.birthday,
            'wechat': staff.person.wechat,
            'qq': staff.person.qq,
            'phone': staff.person.phone,
            'email': staff.person.email,
            'is_admin': staff.is_admin,
            'organization': {
                'id': staff.organization.id,
                'name': staff.organization.name,
            } if staff.organization else {
                'id': -1,
                'name': "",
            },
            'position': {
                'id': staff.position.id,
                'name': staff.position.name,
            } if staff.position else {
                'id': -1,
                "name": "",
            },
            'permission': staff.permission['operation'],
            'account_info': {
                'nick': staff.account.nick,
                'username': staff.account.username,
                'head_url': staff.account.head_url,
                'last_login_time': staff.account.last_login_time,
                'last_login_ip': staff.account.last_login_ip,
                'register_ip': staff.account.register_ip,
                'status': staff.account.status,
                'update_time': staff.account.update_time,
                'create_time': staff.account.create_time,
            },
            'company_info': {
                'id': staff.company.id,
                'name': staff.company.name,
                'license_number': staff.company.license_number,
                'create_time': staff.company.create_time,
            },
        }
        return response


class Update(StaffAuthorizedApi):
    """
    修改个人中心详情
    """
    request = with_metaclass(RequestFieldSet)
    request.myself_info = RequestField(
        DictField,
        desc="员工修改详情",
        conf={
            'name': CharField(desc="姓名", is_required=False),
            'birthday': CharField(desc="生日", is_required=False),
            'gender': CharField(
                desc="性别",
                is_required=False,
                choices=GenderTypes.CHOICES
            ),
            'phone': MobileField(desc="电话", is_required=False),
            'email': CharField(desc="邮箱", is_required=False),
            'wechat': CharField(desc="微信", is_required=False),
            'qq': CharField(desc="QQ", is_required=False),
            'work_number': CharField(desc="员工工号", is_required=False),
            'is_admin': BooleanField(desc="是否是管理员", is_required=False),
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
        StaffServer.update(staff.id, **request.myself_info)

    def fill(self, response):
        return response
