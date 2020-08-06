# coding=UTF-8
import random

from infrastructure.log.base import logger
from infrastructure.utils.common.dictwrapper import DictWrapper
from support.common.generator.base import BaseGenerator
from support.common.generator.helper.business.crm.agent import \
     AgentGenerator

from abs.services.crm.agent.models import Contacts


class ContactsGenerator(BaseGenerator):

    def __init__(self, contacts_infos):
        super(ContactsGenerator, self).__init__()
        self._contacts_infos = self.init(contacts_infos)

    def get_create_list(self, result_mapping):
        contacts_list = []
        agent_list = result_mapping.get(AgentGenerator.get_key())
        for contacts_info in self._contacts_infos:
            contacts_info.update({
                "agent":random.choice(agent_list)
            })
            contacts_list.append(contacts_info)
        return contacts_list

    def create(self, contacts_info, result_mapping):
        contacts_qs = Contacts.query(
            phone = contacts_info.phone,
            agent = contacts_info.agent,
        )
        if contacts_qs.count():
            contacts = contacts_qs[0]
        else:
            contacts = Contacts.create(**contacts_info)
        return contacts

    def delete(self):
        logger.info('================> delete contacts <==================')
        return None
