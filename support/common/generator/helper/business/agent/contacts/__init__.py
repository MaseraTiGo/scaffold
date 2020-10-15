# coding=UTF-8
import random

from abs.services.agent.contract.store.template import Template
from support.common.generator.base import BaseGenerator
from support.common.generator.helper.business.crm.agent import AgentGenerator


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

    def create(self, template_info, result_mapping):
        template_qs = Template.search(name=template_info.name)
        if template_qs.count() > 0:
            return template_qs[0]
        else:
            template = Template.create(
                **template_info
            )
            return template

    def delete(self):
        print('===================>>> delete contacts <====================')
        return None
