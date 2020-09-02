# coding=UTF-8

'''
Created on 2016年7月23日

@author: Administrator
'''

from infrastructure.core.field.base import CharField, DictField, \
        IntField, ListField, DateField, BooleanField, MobileField, \
        DatetimeField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet

from agile.crm.manager.api import StaffAuthorizedApi
from abs.middleware.config import config_middleware
from abs.services.crm.staff.manager import StaffServer
from abs.services.crm.account.manager import StaffAccountServer
from abs.middleground.technology.permission.manager import PermissionServer


class Add(StaffAuthorizedApi):
    """
    添加员工
    """
    request = with_metaclass(RequestFieldSet)
    request.staff_info = RequestField(
        DictField,
        desc = "员工详情",
        conf = {
            'name': CharField(desc = "姓名"),
            'birthday': DateField(desc = "生日", is_required = False),
            'phone': MobileField(desc = "手机"),
            'email': CharField(desc = "邮箱", is_required = False),
            'gender': CharField(
                desc = "性别",
                is_required = False,
                choices = [("男", "man"), ("女", "woman")]
            ),
            'organization_id': IntField(desc = "组织id"),
            'position_id': IntField(desc = "身份id"),
            'remark': CharField(desc = "备注", is_required = False),
        }
    )

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "添加员工接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        organization_id = request.staff_info.pop("organization_id")
        position_id = request.staff_info.pop("position_id")
        staff = StaffServer.create(
            request.staff_info.pop("phone"), \
            **request.staff_info
        )
        appkey = config_middleware.get_value("common", "crm_appkey")
        PermissionServer.bind_position(
            appkey,
            organization_id,
            position_id,
            staff.person_id
        )

    def fill(self, response):
        return response


class Search(StaffAuthorizedApi):
    """
    搜索员工
    """
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(
        IntField,
        desc = "当前页码"
    )
    request.search_info = RequestField(
        DictField,
        desc = "搜索员工条件",
        conf = {
            'name': CharField(desc = "姓名", is_required = False),
            'phone': CharField(desc = "手机", is_required = False),
        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.total = ResponseField(IntField, desc = "数据总数")
    response.total_page = ResponseField(IntField, desc = "总页码数")
    response.data_list = ResponseField(
        ListField,
        desc = "用户列表",
        fmt = DictField(
            desc = "用户详情",
            conf = {
                'id': IntField(desc = "员工编号"),
                'name': CharField(desc = "姓名"),
                'gender': CharField(desc = "性别"),
                'birthday': CharField(desc = "生日"),
                'phone': CharField(desc = "电话"),
                'email': CharField(desc = "邮箱"),
                'work_number': CharField(desc = "员工工号"),
                'is_admin': BooleanField(desc = "是否是管理员"),
                'username': CharField(desc = "账号"),
                'status': CharField(desc = "账号状态"),
                'last_login_time':DatetimeField(desc = "最后登陆时间"),
                'remark': CharField(desc = "备注"),
                'department_role_list': ListField(
                    desc = '所属部门',
                    fmt = DictField(
                        desc = "部门ID",
                        conf = {
                            'department_role_id': IntField(desc = "部门角色id"),
                            'department_id': IntField(desc = "部门id"),
                            'department_name': CharField(desc = "部门名称"),
                            'role_id': IntField(desc = "角色id"),
                            'role_name': CharField(desc = "角色名称"),
                        }
                    )
                )
            }
        )
    )
    response.total = ResponseField(IntField, desc = "数据总数")
    response.total_page = ResponseField(IntField, desc = "总页码数")

    @classmethod
    def get_desc(cls):
        return "搜索员工"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        staff_spliter = StaffServer.search(
            request.current_page,
            **request.search_info
        )
        StaffAccountServer.hung_account(staff_spliter.data)
        return staff_spliter

    def fill(self, response, staff_spliter):
        data_list = [{
            'id': staff.id,
            'name': staff.name,
            'work_number': staff.work_number,
            'gender': staff.person.gender,
            'birthday': staff.person.birthday,
            'phone': staff.person.phone,
            'email': staff.person.email,
            'is_admin': staff.is_admin,
            'username': staff.account.username if \
                        staff.account else '',
            'status':staff.account.status if \
                     staff.account else '',
            'last_login_time':staff.account.last_login_time if \
                              staff.account else None,
            'remark': staff.remark,
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
    """
    获取员工详情接口
    """
    request = with_metaclass(RequestFieldSet)
    request.staff_id = RequestField(IntField, desc = "员工id")

    response = with_metaclass(ResponseFieldSet)
    response.staff_info = ResponseField(
        DictField,
        desc = "用户详情",
        conf = {
            'id': IntField(desc = "员工编号"),
            'name': CharField(desc = "姓名"),
            'gender': CharField(desc = "性别"),
            'birthday': CharField(desc = "生日"),
            'phone': CharField(desc = "电话"),
            'email': CharField(desc = "邮箱"),
            'work_number': CharField(desc = "员工工号"),
            'is_admin': BooleanField(desc = "是否是管理员"),

            # 'department_role_list': ListField(
                # desc = '所属部门',
                # is_required = False,
                # fmt = DictField(
                    # desc = "部门ID",
                    # conf = {
                        # 'department_role_id': IntField(desc = "部门角色id"),
                        # 'department_id': IntField(desc = "部门id"),
                        # 'department_name': CharField(desc = "部门名称"),
                        # 'role_id': IntField(desc = "部门id"),
                        # 'role_name': CharField(desc = "角色名称"),
                    # }
                # )
            # ),

        }
    )

    @classmethod
    def get_desc(cls):
        return "获取员工详情接口"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        return StaffServer.get(request.staff_id)

    def fill(self, response, staff):
        '''
        department_role_list = [{
            'role_id': department_role.role.id,
            'role_name': department_role.role.name,
            'department_id': department_role.department.id,
            'department_name': department_role.department.name,
            'department_role_id': department_role.id,
        } for department_role in staff.department_role_list]
        '''
        response.staff_info = {
            'id': staff.id,
            'name': staff.person.name,
            'work_number': staff.work_number,
            'gender': staff.person.gender,
            'birthday': staff.person.birthday,
            'phone': staff.person.phone,
            'email': staff.person.email,
            'is_admin': staff.is_admin,
            # 'department_role_list': department_role_list
        }
        return response


class Update(StaffAuthorizedApi):
    """
    修改员工信息
    """
    request = with_metaclass(RequestFieldSet)
    request.staff_id = RequestField(IntField, desc = "员工id")
    request.staff_info = RequestField(
        DictField,
        desc = "员工修改详情",
        conf = {
            'name': CharField(desc = "姓名", is_required = False),
            'gender': CharField(desc = "性别", is_required = False),
            'birthday': CharField(desc = "生日", is_required = False),
            'phone': MobileField(desc = "电话", is_required = False),
            'email': CharField(desc = "邮箱", is_required = False),
            'remark': CharField(desc = "备注", is_required = False),
        }
    )

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "员工个人中心修改接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        StaffServer.update(request.staff_id, **request.staff_info)

    def fill(self, response):
        return response
