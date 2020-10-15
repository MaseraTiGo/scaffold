# coding=UTF-8
import random

from abs.services.agent.customer.store.customer import AgentCustomer
from support.common.generator.base import BaseGenerator
from support.common.generator.helper import PersonGenerator, AgentGenerator


class CustomerGenerator(BaseGenerator):

    def __init__(self, contacts_info):
        super(CustomerGenerator, self).__init__()
        self._contacts_info = self.init(contacts_info)

    def get_create_list(self, result_mapping):
        agent_list = result_mapping.get(AgentGenerator.get_key())
        person_list = result_mapping.get(PersonGenerator.get_key())
        contacts_list = []
        for contacts_info in self._contacts_info:
            company = random.choice(agent_list)
            person = random.choice(person_list)
            contacts_info.update({
                'agent_id': company.id,
                'person_id': person.id,
            })
            contacts_list.append(contacts_info)
        return contacts_list

    def create(self, agent_customer_info, result_mapping):
        template_qs = AgentCustomer.search(phone=agent_customer_info.phone)
        if template_qs.count() > 0:
            return template_qs[0]
        else:
            template = AgentCustomer.create(
                **agent_customer_info
            )
            return template

    def delete(self):
        print('===================>>> delete agent customer <====================')
        return None
