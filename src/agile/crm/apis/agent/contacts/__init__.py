# coding=UTF-8

from infrastructure.core.field.base import CharField, DictField, \
        IntField, ListField, DatetimeField, BooleanField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet
from infrastructure.core.exception.business_error import BusinessError
from abs.middleground.business.person.utils.constant import GenderTypes
from abs.middleground.business.account.utils.constant import StatusTypes
from agile.crm.manager.api import StaffAuthorizedApi
from abs.services.crm.agent.manager import AgentServer
from abs.services.agent.staff.manager import AgentStaffServer
from abs.services.agent.account.manager import AgentStaffAccountServer


class Add(StaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.agent_id = RequestField(IntField, desc = "代理商id")
    request.contacts_info = RequestField(
        DictField,
        desc = "联系人信息",
        conf = {
            'contacts': CharField(desc = "联系人"),
            'phone': CharField(desc = "联系电话"),
            'email': CharField(desc = "联系邮箱"),
            'gender': CharField(desc = "性别"),
        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.contacts_id = ResponseField(IntField, desc = "联系人ID")

    @classmethod
    def get_desc(cls):
        return "代理商联系人添加接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        agent = AgentServer.get(request.agent_id)
        request.contacts_info.update({
           "agent":agent
        })
        contacts = AgentServer.create_contacts(
           **request.contacts_info
        )
        return contacts

    def fill(self, response, contacts):
        response.contacts_id = contacts.id
        return response


class Search(StaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc = "当前页面")
    request.agent_id = RequestField(IntField, desc = "代理商id")
    request.search_info = RequestField(
        DictField,
        desc = "搜索联系人",
        conf = {

        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.total = ResponseField(IntField, desc = "数据总数")
    response.total_page = ResponseField(IntField, desc = "总页码数")
    response.data_list = ResponseField(
        ListField,
        desc = "联系人列表",
        fmt = DictField(
            desc = "联系人内容",
            conf = {
                'id': IntField(desc = "联系人id"),
                'contacts': CharField(desc = "联系人"),
                'phone': CharField(desc = "联系电话"),
                'email': CharField(desc = "联系邮箱"),
                'gender': CharField(
                    desc = "性别",
                    choices = GenderTypes.CHOICES
                ),
                'account': CharField(desc = "账号"),
                'account_status': CharField(
                    desc = "账号状态",
                    choices = StatusTypes.CHOICES
                ),
                'create_time': DatetimeField(desc = "添加时间"),
            }
        )
    )

    @classmethod
    def get_desc(cls):
        return "代理商联系人搜索接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        agent = AgentServer.get(request.agent_id)
        request.search_info.update({
            "agent":agent
        })
        spliter = AgentServer.search_contacts(
            request.current_page,
            **request.search_info
        )
        return spliter

    def fill(self, response, spliter):
        data_list = [{
                "id":contacts.id,
                "contacts":contacts.contacts,
                "phone":contacts.phone,
                "email":contacts.email,
                "gender":contacts.gender,
                "account":contacts.account,
                "account_status":contacts.account_status,
                "create_time":contacts.create_time,
              } for contacts in spliter.data]
        response.data_list = data_list
        response.total = spliter.total
        response.total_page = spliter.total_page
        return response


class Update(StaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.contacts_id = RequestField(IntField, desc = "代理商id")
    request.contacts_info = RequestField(
        DictField,
        desc = "联系人信息",
        conf = {
            'contacts': CharField(desc = "联系人"),
            'phone': CharField(desc = "联系电话"),
            'email': CharField(desc = "联系邮箱"),
            'gender': CharField(desc = "性别"),
        }
    )
    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "代理商联系人信息更新接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        contacts = AgentServer.update_contacts(
            request.contacts_id,
            **request.contacts_info
        )

    def fill(self, response):
        return response


class AddAccount(StaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.contacts_id = RequestField(IntField, desc = "代理商id")
    request.contacts_info = RequestField(
        DictField,
        desc = "联系人账号信息",
        conf = {
            'account': CharField(desc = "账号"),
            'password': CharField(desc = "密码"),
        }
    )
    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "代理商联系人账号生成接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        contacts = AgentServer.get_contacts(request.contacts_id)
        if contacts.account:
            raise BusinessError("请不要重复生成账号")
        add_staff_info = {
            "name":contacts.contacts,
            "email":contacts.email,
            "gender":contacts.gender,
            "is_admin":True,
        }
        agent_staff = AgentStaffServer.create(
            contacts.phone,
            contacts.agent,
            **add_staff_info
        )
        add_account_info = {
            "username":request.contacts_info["account"],
            "password":request.contacts_info["password"],
            "role_id":agent_staff.id
        }
        AgentStaffAccountServer.create(**add_account_info)
        contacts.update(
            account = request.contacts_info["account"],
        )

    def fill(self, response):
        return response
