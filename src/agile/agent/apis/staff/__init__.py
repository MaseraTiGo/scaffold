# coding=UTF-8

'''
Created on 2016年7月23日

@author: Administrator
'''
import json
from infrastructure.core.field.base import CharField, DictField, \
        IntField, ListField, DateField, BooleanField, MobileField, \
        DatetimeField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet

from agile.agent.manager.api import AgentStaffAuthorizedApi
from abs.middleground.business.person.utils.constant import\
     GenderTypes

from abs.services.agent.staff.manager import AgentStaffServer
from abs.services.agent.account.manager import AgentStaffAccountServer


class Add(AgentStaffAuthorizedApi):
    """
    添加员工
    """
    request = with_metaclass(RequestFieldSet)
    request.staff_info = RequestField(
        DictField,
        desc = "员工详情",
        conf = {
            'name': CharField(desc = "姓名"),
            'identification': CharField(desc = "身份证号"),
            'phone': CharField(desc = "手机"),
            'organization_id': IntField(desc = "组织id"),
            'position_id': IntField(desc = "身份id"),
            'entry_time':DateField(desc = "入职时间", is_required = False),
            'address': CharField(desc = "家庭住址", is_required = False),
            'emergency_contact': CharField(desc = "紧急联系人", is_required = False),
            'emergency_phone': CharField(desc = "紧急联系人电话", is_required = False),
            'education': CharField(desc = "学历", is_required = False),
            'bank_number': CharField(desc = "银行卡号", is_required = False),
            'contract': CharField(desc = "合同编号", is_required = False),
            'email': CharField(desc = "邮箱", is_required = False),
            'gender': CharField(
                desc = "性别",
                choices = GenderTypes.CHOICES
            ),
            'diploma_img':ListField(
                desc = '毕业证书',
                fmt = CharField(desc = "毕业证书"),
                is_required = False
            ),
        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.agent_staff_id = ResponseField(IntField, desc = "当前页码")

    @classmethod
    def get_desc(cls):
        return "添加员工接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        agent = self.auth_agent
        if "diploma_img" in request.staff_info:
            diploma_img = request.staff_info.pop("diploma_img")
            request.staff_info.update({
                "diploma_img":json.dumps(diploma_img)
            })
        agent_staff = AgentStaffServer.create(
            request.staff_info.pop("phone"), \
            agent, \
            **request.staff_info
        )
        return agent_staff

    def fill(self, response, agent_staff):
        response.agent_staff_id = agent_staff.id
        return response


class Search(AgentStaffAuthorizedApi):
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
                'nick': CharField(desc = "昵称"),
                'head_url': CharField(desc = "头像"),
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
        auth = self.auth_user
        request.search_info.update({
            "agent_id":auth.agent_id
        })
        staff_spliter = AgentStaffServer.search(
            request.current_page,
            **request.search_info
        )
        AgentStaffAccountServer.hung_account(staff_spliter.data)
        return staff_spliter

    def fill(self, response, staff_spliter):
        data_list = [{
            'id': staff.id,
            'nick': staff.nick,
            'head_url': staff.head_url,
            'name': staff.person.name,
            'work_number': staff.work_number,
            'gender': staff.person.gender,
            'birthday': staff.person.birthday,
            'phone': staff.person.phone,
            'email': staff.person.email,
            'is_admin': staff.is_admin,
            'username': staff.account.username if \
                        staff.account else "",
            'status':staff.account.status if \
                     staff.account else "",
            'last_login_time':staff.account.last_login_time if \
                              staff.account else None,
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


class Get(AgentStaffAuthorizedApi):
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
            'id':IntField(desc = "员工id"),
            'name': CharField(desc = "姓名"),
            'identification': CharField(desc = "身份证号"),
            'phone': CharField(desc = "手机"),
            'organization_id': IntField(desc = "组织id"),
            'organization_name': IntField(desc = "组织名称"),
            'position_id': IntField(desc = "身份名称"),
            'position_name': IntField(desc = "身份id"),
            'entry_time':DateField(desc = "入职时间"),
            'address': CharField(desc = "家庭住址"),
            'emergency_contact': CharField(desc = "紧急联系人"),
            'emergency_phone': CharField(desc = "紧急联系人电话"),
            'education': CharField(desc = "学历"),
            'bank_number': CharField(desc = "银行卡号"),
            'contract': CharField(desc = "合同编号"),
            'email': CharField(desc = "邮箱"),
            'gender': CharField(
                desc = "性别",
                choices = GenderTypes.CHOICES
            ),
            'diploma_img':ListField(
                desc = '毕业证书',
                fmt = CharField(desc = "毕业证书")
            ),
        }
    )

    @classmethod
    def get_desc(cls):
        return "获取员工详情接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        agent_staff = AgentStaffServer.get(request.staff_id)
        return agent_staff

    def fill(self, response, agent_staff):
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
            'id':agent_staff.id,
            'name': agent_staff.name,
            'identification': agent_staff.identification,
            'phone': agent_staff.phone,
            'organization_id': 1,
            'organization_name':'公司',
            'position_id':1,
            'position_name':'超级管理员',
            'entry_time':agent_staff.entry_time,
            'address': agent_staff.address,
            'emergency_contact': agent_staff.emergency_contact,
            'emergency_phone':agent_staff.emergency_phone,
            'education': agent_staff.education,
            'bank_number': agent_staff.bank_number,
            'contract': agent_staff.contract,
            'email': agent_staff.person.email,
            'gender': agent_staff.person.gender,
            'diploma_img':json.loads(agent_staff.diploma_img),
        }
        return response


class Update(AgentStaffAuthorizedApi):
    """
    修改员工信息
    """
    request = with_metaclass(RequestFieldSet)
    request.staff_id = RequestField(IntField, desc = "员工id")
    request.staff_info = RequestField(
        DictField,
        desc = "员工修改详情",
        conf = {
            'name': CharField(desc = "姓名"),
            'identification': CharField(desc = "身份证号"),
            'phone': CharField(desc = "手机"),
            'organization_id': IntField(desc = "组织id"),
            'position_id': IntField(desc = "身份id"),
            'entry_time':DateField(desc = "入职时间", is_required = False),
            'address': CharField(desc = "家庭住址", is_required = False),
            'emergency_contact': CharField(desc = "紧急联系人", is_required = False),
            'emergency_phone': CharField(desc = "紧急联系人电话", is_required = False),
            'education': CharField(desc = "学历", is_required = False),
            'bank_number': CharField(desc = "银行卡号", is_required = False),
            'contract': CharField(desc = "合同编号", is_required = False),
            'email': CharField(desc = "邮箱", is_required = False),
            'gender': CharField(
                desc = "性别",
                choices = GenderTypes.CHOICES
            ),
            'diploma_img':ListField(
                desc = '毕业证书',
                fmt = CharField(desc = "毕业证书"),
                is_required = False
            ),
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
        if "diploma_img" in request.staff_info:
            diploma_img = request.staff_info.pop("diploma_img")
            request.staff_info.update({
                "diploma_img":json.dumps(diploma_img)
            })
        agent_staff = AgentStaffServer.update(
            request.staff_id,
            **request.staff_info
        )

    def fill(self, response):
        return response
