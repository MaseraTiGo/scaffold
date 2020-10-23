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
from abs.middleground.business.account.utils.constant import StatusTypes
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
            'qq': CharField(desc = "qq", is_required = False),
            'wechat': CharField(desc = "微信", is_required = False),
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
        staff = self.auth_user
        organization_id = request.staff_info.pop('organization_id')
        position_id = request.staff_info.pop('position_id')
        request.staff_info.update({
            "work_number":StaffServer.generate_work_number(staff.company)
        })
        new_staff = StaffServer.create(
            request.staff_info.pop("phone"),
            company = staff.company,
            **request.staff_info
        )
        permission = PermissionServer.bind_position(
            staff.company.permission_key,
            organization_id,
            position_id,
            # new_staff.id
            new_staff.person_id
        )
        StaffServer.update(
            new_staff.id,
            permission_id = permission.id,
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
                'wechat': CharField(desc = "微信"),
                'qq': CharField(desc = "QQ"),
                'phone': CharField(desc = "电话"),
                'email': CharField(desc = "邮箱"),
                'work_number': CharField(desc = "员工工号"),
                'is_admin': BooleanField(desc = "是否是管理员"),
                'username': CharField(desc = "账号"),
                'status': CharField(desc = "账号状态"),
                'last_login_time':DatetimeField(desc = "最后登陆时间"),
                'remark': CharField(desc = "备注"),
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
                'create_time': DatetimeField(desc = "创建时间"),
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
        staff = self.auth_user
        request.search_info.update({
            "company":staff.company
        })
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
            'wechat': staff.person.wechat,
            'qq': staff.person.qq,
            'phone': staff.phone,
            'email': staff.person.email,
            'is_admin': staff.is_admin,
            'username': staff.account.username if \
                        staff.account else '',
            'status':staff.account.status if \
                     staff.account else '',
            'last_login_time':staff.account.last_login_time if \
                              staff.account else None,
            'remark': staff.remark,
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
            'create_time': staff.create_time,
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
            'wechat': CharField(desc = "微信"),
            'qq': CharField(desc = "QQ"),
            'phone': CharField(desc = "电话"),
            'email': CharField(desc = "邮箱"),
            'work_number': CharField(desc = "员工工号"),
            'is_admin': BooleanField(desc = "是否是管理员"),
            'update_time': DatetimeField(desc = "更新时间"),
            'create_time': DatetimeField(desc = "创建时间"),
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
            'account_info': DictField(
                desc = "账号信息",
                conf = {
                    'nick': CharField(desc = "昵称"),
                    'username': CharField(desc = "账户"),
                    'head_url': CharField(desc = "头像"),
                    'last_login_time': DatetimeField(desc = "最后登录时间"),
                    'last_login_ip': CharField(desc = "最后登录ip"),
                    'register_ip': CharField(desc = "注册ip"),
                    'status': CharField(
                        desc = "状态",
                        is_required = False,
                        choices = StatusTypes.CHOICES
                    ),
                    'update_time': DatetimeField(desc = "更新时间"),
                    'create_time': DatetimeField(desc = "创建时间"),
                }
            ),
            'company_info': DictField(
                desc = "账号信息",
                conf = {
                    'id': IntField(desc = "id"),
                    'name': CharField(desc = "昵称"),
                    'license_number': CharField(desc = "营业执照"),
                    'create_time': DatetimeField(desc = "创建时间"),
                }
            )
        }
    )

    @classmethod
    def get_desc(cls):
        return "获取员工详情接口"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        staff_id = request.staff_id
        staff = StaffServer.get(staff_id)
        staff.account = StaffAccountServer.get(staff_id)
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
            'update_time': staff.update_time,
            'create_time': staff.create_time,
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
            # 'phone': MobileField(desc = "电话", is_required = False),
            'email': CharField(desc = "邮箱", is_required = False),
            'qq': CharField(desc = "qq", is_required = False),
            'wechat': CharField(desc = "微信", is_required = False),
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


class Bind(StaffAuthorizedApi):
    """
    绑定员工信息到部门及岗位
    """
    request = with_metaclass(RequestFieldSet)
    request.staff_id = RequestField(IntField, desc = "员工id")
    request.organization_id = RequestField(IntField, desc = "组织id")
    request.position_id = RequestField(IntField, desc = "岗位id")

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        staff_id = self.auth_user.id
        staff = StaffServer.get(staff_id)
        tobe_modified_staff = StaffServer.get(request.staff_id)
        permission = PermissionServer.bind_position(
            staff.company.permission_key,
            request.organization_id,
            request.position_id,
            tobe_modified_staff.person_id,
        )
        StaffServer.update_staff_permission_id(tobe_modified_staff, permission)


    def fill(self, response):
        return response
