# coding=UTF-8

'''
Created on 2020年6月18日

@author: Roy
'''

from infrastructure.core.field.base import CharField, DictField, IntField, ListField, DatetimeField, DateField, BooleanField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet
from infrastructure.core.exception.business_error import BusinessError

from agile.apis.base import StaffAuthorizedApi
from agile.apis.base import NoAuthrizedApi
from abs.service.staff.manager import StaffServer



class Get(StaffAuthorizedApi):
    """获取个人中心详情"""
    request = with_metaclass(RequestFieldSet)

    response = with_metaclass(ResponseFieldSet)
    response.staff_info = ResponseField(DictField, desc = "用户详情", conf = {
        'name': CharField(desc = "姓名"),
        'identification': CharField(desc = "身份证"),
        'gender': CharField(desc = "性别"),
        'birthday': CharField(desc = "生日"),
        'phone': CharField(desc = "电话"),
        'email': CharField(desc = "邮箱"),
        'id_number': CharField(desc = "员工工号"),
        'is_admin': BooleanField(desc = "是否是管理员"),
        'department_role_list': ListField(desc = '所属部门', is_required = False, fmt =
                                          DictField(desc = "部门ID", conf = {
                                            'department_role_id': IntField(desc = "部门角色id"),
                                            'department_id': IntField(desc = "部门id"),
                                            'department_name': CharField(desc = "部门名称"),
                                            'role_id': IntField(desc = "部门id"),
                                            'role_name': CharField(desc = "角色名称"),
                                          })),
    })

    @classmethod
    def get_desc(cls):
        return "员工个人中心详情接口"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        return StaffServer.get(self.auth_user)

    def fill(self, response, staff):
        department_role_list = [ {
            'role_id': department_role.role.id,
            'role_name': department_role.role.name,
            'department_id': department_role.department.id,
            'department_name': department_role.department.name,
            'department_role_id': department_role.id,
        } for department_role in staff.department_role_list]
        response.staff_info = {
            'name': staff.certification.name,
            'id_number': staff.id_number,
            'identification': staff.certification.identification,
            'gender': staff.certification.gender,
            'birthday': staff.certification.birthday,
            'phone': staff.certification.phone,
            'email': staff.certification.email,
            'is_admin': staff.is_admin,
            'department_role_list': department_role_list
        }
        return response


class Update(StaffAuthorizedApi):
    """修改个人中心详情"""
    request = with_metaclass(RequestFieldSet)
    request.myself_info = RequestField(DictField, desc = "员工修改详情", conf = {
        'name': CharField(desc = "姓名"),
        'identification': CharField(desc = "身份证"),
        'gender': CharField(desc = "性别"),
        'birthday': CharField(desc = "生日"),
        'phone': CharField(desc = "电话"),
        'email': CharField(desc = "邮箱"),
        'id_number': CharField(desc = "员工工号"),
        'is_admin': BooleanField(desc = "是否是管理员"),
    })

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
