# coding=UTF-8

from infrastructure.core.exception.business_error import BusinessError
from infrastructure.utils.common.split_page import Splitor

from abs.common.manager import BaseManager
from abs.middleground.business.enterprise.assistor.link.manager import\
        AbstractCompanyServer
from abs.middleground.business.person.assistor.staff.manager import\
        AbstractStaffServer
from abs.middleground.business.enterprise.manager import EnterpriseServer
from abs.middleground.technology.permission.manager import PermissionServer
from abs.services.agent.agent.models import Agent, Contacts, Staff


class AgentServer(AbstractCompanyServer):

    COMPANY_MODEL = Agent

    @classmethod
    def hung_enterprise(cls, agent_list):
        agent_mapping = {}
        for agent in agent_list:
            agent.enterprise = None
            agent_mapping[agent.company_id] = agent
        enterprise_qs = EnterpriseServer.get_byids(agent_mapping.keys())
        for enterprise in enterprise_qs:
            if enterprise.id in agent_mapping:
                agent_mapping[enterprise.id].enterprise = enterprise
        return agent_list

    @classmethod
    def search(cls, current_page, **search_info):
        splitor = super().search(current_page, **search_info)
        return splitor

    @classmethod
    def search_all(cls, **search_info):
        agent_qs = Agent.search(**search_info)
        return agent_qs

    @classmethod
    def get(cls, agent_id):
        agent = super().get(agent_id)
        cls.hung_enterprise([agent])
        return agent

    @classmethod
    def update(cls, agent_id, **update_info):
        agent = super().update(agent_id, **update_info)
        return agent

    @classmethod
    def hung_agent(cls, obj_list):
        obj_mapping = {}
        for obj in obj_list:
            obj.agent = None
            if obj.agent_id not in obj_mapping:
                obj_mapping[obj.agent_id] = []
            obj_mapping[obj.agent_id].append(obj)
        agent_qs = cls.search_all(id__in = obj_mapping.keys())
        for agent in agent_qs:
            if agent.id in obj_mapping:
                for obj in obj_mapping[agent.id]:
                    obj.agent = agent
        return obj_list


    @classmethod
    def create_contacts(cls, **contacts_info):
        contacts = None
        contacts_qs = cls.search_all_contacts(
           agent = contacts_info["agent"],
        )
        if contacts_qs.count() >= 3:
            raise BusinessError("此代理商联系人添加超过上限")
        if cls.is_exist_contacts(
           contacts_info["phone"],
           contacts_info["agent"],
        ):
            contacts = Contacts.create(**contacts_info)
        return contacts

    @classmethod
    def search_contacts(cls, current_page, **search_info):
        contacts_qs = cls.search_all_contacts(**search_info).\
                          order_by("-create_time")
        splitor = Splitor(current_page, contacts_qs)
        return splitor

    @classmethod
    def search_all_contacts(cls, **search_info):
        contacts_qs = Contacts.search(**search_info)
        return contacts_qs

    @classmethod
    def get_contacts(cls, contacts_id):
        contacts = Contacts.get_byid(contacts_id)
        if contacts is None:
            raise BusinessError("此联系人不存在")
        return contacts

    @classmethod
    def is_exist_contacts(cls, phone, agent, contacts = None):
        contacts_qs = cls.search_all_contacts(
           agent = agent,
           phone = phone
        )
        if contacts:
            contacts_qs = contacts_qs.exclude(id = contacts.id)
        if contacts_qs.count() > 0:
            raise BusinessError("此联系人已存在")
        return True

    @classmethod
    def update_contacts(cls, contact_id, **update_info):
        contacts = cls.get_contacts(contact_id)
        if cls.is_exist_contacts(
          update_info["phone"],
          contacts.agent,
          contacts
        ):
            contacts.update(**update_info)
        return contacts


class AgentStaffServer(AbstractStaffServer):

    STAFF_MODEL = Staff

    @classmethod
    def check_phone(cls, phone):
        staff_qs = Staff.search(phone = phone)
        if staff_qs.count() > 0:
            return True
        return False

    @classmethod
    def generate_work_number(cls, company):
        count_num = Staff.search(company = company).count()
        work_number = "BQ" + str(10000000 + count_num + 1)
        return work_number

    @classmethod
    def get_permission(self, staff):
        permission = PermissionServer.get_permission(
                staff.company.permission_key,
                staff.id,
                staff.is_admin
            )
        return permission

    @classmethod
    def hung_staff(cls, obj_list):
        obj_mapping = {}
        for obj in obj_list:
            obj.staff = None
            if obj.staff_id not in obj_mapping:
                obj_mapping[obj.staff_id] = []
            obj_mapping[obj.staff_id].append(obj)
        staff_qs = Staff.search(id__in = obj_mapping.keys())
        for staff in staff_qs:
            if staff.id in obj_mapping:
                for obj in obj_mapping[staff.id]:
                    obj.staff = staff
        return obj_list

    '''
    @classmethod
    def hung_permission(cls, staff_list):
        for staff in staff_list:
            staff.department_role_list = []
        return staff_list

    @classmethod
    def get(cls, staff_id):
        staff = Staff.get_byid(staff_id)
        PersonServer.hung_persons([staff])
        cls.hung_permission([staff])
        return staff

    @classmethod
    def search(cls, current_page, **search_info):
        if "name" in search_info:
            name = search_info.pop("name")
            search_info.update({"name__contains":name})
        staff_qs = Staff.search(**search_info)
        staff_qs.order_by('-create_time')
        splitor = Splitor(current_page, staff_qs)
        PersonServer.hung_persons(splitor.get_list())
        cls.hung_permission(splitor.get_list())
        return splitor

    @classmethod
    def is_exsited(cls, phone):
        is_exsited, staff = Staff.is_exsited(phone)
        return is_exsited, staff

    @classmethod
    def generate_work_number(cls, company_id):
        count_num = Staff.search(company_id = company_id).count()
        work_number = "CL" + str(10000000 + count_num)
        return work_number

    @classmethod
    def create(cls, phone, agent, **staff_info):
        is_person_exsited, person = PersonServer.is_exsited(phone)
        if is_person_exsited:
            raise BusinessError('客户已存在，不能创建')

        person = PersonServer.create(phone = phone, **staff_info)
        staff = Staff.create(
            work_number = cls.generate_work_number(agent.company_id),
            person_id = person.id,
            company_id = agent.company_id,
            agent_id = agent.id,
            phone = phone,
            **staff_info
        )
        return staff

    @classmethod
    def update(cls, staff_id, **update_info):
        staff = cls.get(staff_id)
        is_person_exsited, person = PersonServer.is_exsited(
            update_info["phone"]
        )
        if is_person_exsited:
            if person.id != staff.person_id:
                raise BusinessError('手机号已存在')
        PersonServer.update(staff.person_id, **update_info)
        staff.update(**update_info)
        return staff
    '''