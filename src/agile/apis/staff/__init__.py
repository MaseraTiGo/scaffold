# coding=UTF-8

'''
Created on 2016年7月23日

@author: Administrator
'''

from infrastructure.core.field.base import CharField, DictField, IntField, ListField, DatetimeField, DateField, BooleanField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet
from infrastructure.core.exception.business_error import BusinessError

from agile.apis.base import StaffAuthorizedApi
from agile.apis.base import NoAuthrizedApi
from abs.service.staff.manager import StaffServer


# class Add(StaffAuthorizedApi):
class Add(NoAuthrizedApi):
    """添加员工"""
    request = with_metaclass(RequestFieldSet)
    request.staff_info = RequestField(DictField, desc = "员工详情", conf = {
        'name': CharField(desc = "姓名"),
        'birthday': DateField(desc = "生日", is_required = False),
        'phone': CharField(desc = "手机", is_required = False),
        'email': CharField(desc = "邮箱", is_required = False),
        'gender': CharField(desc = "性别", is_required = False, \
                            choices = [("男", "man"), ("女","woman")]),
        'identification': CharField(desc = "身份证", is_required = False),
        'entry_time': DateField(desc = "入职时间", is_required = False),
        'education': CharField(desc = "学历", is_required = False),
        'remark': CharField(desc = "备注", is_required = False),
        'role_ids': ListField(desc = '所属角色', is_required = False, fmt = IntField(desc = "角色ID")),
        'department_ids': ListField(desc = '所属部门', is_required = False, fmt = IntField(desc = "部门ID")),
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "添加员工接口"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        print(request.staff_info)

    def fill(self, response):
        return response



class Search(NoAuthrizedApi):
    """搜索员工"""
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc = "当前页码")
    request.search_info = RequestField(DictField, desc = "搜索员工条件", conf = {
        'name': CharField(desc = "姓名", is_required = False),
        'phone': CharField(desc = "手机", is_required = False),
    })

    response = with_metaclass(ResponseFieldSet)
    response.total = ResponseField(IntField, desc = "数据总数")
    response.total_page = ResponseField(IntField, desc = "总页码数")
    response.data_list = ResponseField(ListField, desc = "用户列表", fmt = \
                                       DictField(desc = "用户详情", conf = {
                                            'id': IntField(desc = "员工编号"),
                                            'name': CharField(desc = "姓名"),
                                            'identification': CharField(desc = "身份证"),
                                            'gender': CharField(desc = "性别"),
                                            'birthday': CharField(desc = "生日"),
                                            'phone': CharField(desc = "电话"),
                                            'email': CharField(desc = "邮箱"),
                                            'id_number': CharField(desc = "员工工号"),
                                            'is_admin': BooleanField(desc = "是否是管理员"),
                                            'department_role_list': \
                                                ListField(desc = '所属部门', fmt =
                                                    DictField(desc = "部门ID", conf = {
                                                        'department_role_id': IntField(desc = "部门角色id"),
                                                        'department_id': IntField(desc = "部门id"),
                                                        'department_name': CharField(desc = "部门名称"),
                                                        'role_id': IntField(desc = "部门id"),
                                                        'role_name': CharField(desc = "角色名称"),
                                                    })
                                                )
                                            }))
    response.total = ResponseField(IntField, desc = "数据总数")
    response.total_page = ResponseField(IntField, desc = "总页码数")


    @classmethod
    def get_desc(cls):
        return "搜索员工"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        staff_spliter = StaffServer.search(request.current_page, **request.search_info)
        return staff_spliter

    def fill(self, response, staff_spliter):
        data_list = [{
            'id': staff.id,
            'name': staff.certification.name,
            'id_number': staff.id_number,
            'identification': staff.certification.identification,
            'gender': staff.certification.gender,
            'birthday': staff.certification.birthday,
            'phone': staff.certification.phone,
            'email': staff.certification.email,
            'is_admin': staff.is_admin,
            'department_role_list': [{
                'role_id': department_role.role.id,
                'role_name': department_role.role.name,
                'department_id': department_role.department.id,
                'department_name': department_role.department.name,
                'department_role_id': department_role.id,
            } for department_role in staff.department_role_list]
        } for staff in staff_spliter.data]
        response.data_list = data_list
        response.total = staff_spliter.total
        response.total_page = staff_spliter.total_page
        return response


class Get(StaffAuthorizedApi):
    """获取员工详情接口"""
    request = with_metaclass(RequestFieldSet)
    request.staff_id = RequestField(IntField, desc = "员工id")

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
        return "获取员工详情接口"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        return StaffServer.get_byid(request.staff_id)

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
    """修改员工信息"""
    request = with_metaclass(RequestFieldSet)
    request.staff_id = RequestField(IntField, desc = "员工id")
    request.staff_info = RequestField(DictField, desc = "员工修改详情", conf = {
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
        StaffServer.update(request.staff_id, **request.staff_info)

    def fill(self, response):
        return response
