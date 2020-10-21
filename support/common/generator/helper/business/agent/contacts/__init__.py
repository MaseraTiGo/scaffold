# coding=UTF-8
import random

from abs.services.agent.agent.store.contacts import Contacts
from support.common.generator.base import BaseGenerator
from support.common.generator.helper.business.crm.agent import AgentGenerator
# from support.common.generator.helper.business.agent.staff import AgentStaffGenerator


class ContactsGenerator(BaseGenerator):

    def __init__(self, contacts_info):
        super(ContactsGenerator, self).__init__()
        self._contacts_info = self.init(contacts_info)

    def get_create_list(self, result_mapping):
        agent_list = result_mapping.get(AgentGenerator.get_key())

        contacts_list = []
        for contacts_info in self._contacts_info:
            company = random.choice(agent_list)
            contacts_info.update({
                'agent': company,
            })
            contacts_list.append(contacts_info)
        return contacts_list

    def create(self, contacts_info, result_mapping):
        contacts_qs = Contacts.search(phone=contacts_info.phone)
        if contacts_qs.count() > 0:
            return contacts_qs[0]
        else:
            contacts = Contacts.create(
                **contacts_info
            )
            return contacts

    def delete(self):
        print('===================>>> delete contacts <====================')
        return None
