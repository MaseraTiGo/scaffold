# coding=UTF-8

from infrastructure.core.exception.business_error import BusinessError
from infrastructure.utils.common.split_page import Splitor

from abs.common.manager import BaseManager
from abs.middleground.business.enterprise.manager import EnterpriseServer
from abs.services.crm.agent.models import Agent, Contacts


class AgentServer(BaseManager):

    @classmethod
    def create(cls, **agent_info):
        agent = None
        enterprise_infos = {
            "name":agent_info["name"],
            "license_number":agent_info.pop("license_code"),
            "license_url":agent_info.pop("license_picture"),
        }
        enterprise = EnterpriseServer.create(
            **enterprise_infos
        )
        if enterprise:
            if cls.is_exist(enterprise.id):
                agent_info.update({"company_id":enterprise.id})
                agent = Agent.create(**agent_info)
        return agent

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
        agent_qs = cls.search_all(**search_info).\
                       order_by("-create_time")
        splitor = Splitor(current_page, agent_qs)
        cls.hung_enterprise(splitor.data)
        return splitor

    @classmethod
    def search_all(cls, **search_info):
        agent_qs = Agent.search(**search_info)
        return agent_qs

    @classmethod
    def get(cls, agent_id):
        agent = Agent.get_byid(agent_id)
        if agent is None:
            raise BusinessError("此代理商不存在")
        cls.hung_enterprise([agent])
        return agent

    @classmethod
    def is_exist(cls, company_id):
        agent_qs = cls.search_all(company_id = company_id)
        if agent_qs.count() > 0:
            raise BusinessError("此代理商信用编码重复")
        return True

    @classmethod
    def update(cls, agent_id, **update_info):
        enterprise_infos = {
            "name":update_info.pop("name"),
            "license_number":update_info.pop("license_code"),
            "license_url":update_info.pop("license_picture"),
        }
        agent = cls.get(agent_id)
        EnterpriseServer.update(agent.company_id, **enterprise_infos)
        agent.update(**update_info)
        return agent


    @classmethod
    def create_contacts(cls, **contacts_info):
        contacts = None
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
