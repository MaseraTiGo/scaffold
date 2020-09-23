# coding=UTF-8

import random

from support.common.generator.base import BaseGenerator
from support.common.generator.helper import EnterpriseGenerator, \
        PersonGenerator, AgentGenerator
from abs.middleground.business.person.models import Person
from abs.services.agent.agent.models import Staff


class AgentStaffGenerator(BaseGenerator):

    def __init__(self, staff_info):
        super(AgentStaffGenerator, self).__init__()
        self._staff_infos = self.init(staff_info)

    def get_create_list(self, result_mapping):
        staff_list = []
        agent_list = result_mapping.get(AgentGenerator.get_key())
        for staff_info in self._staff_infos:
            staff_info.update({
                "agent_id":random.choice(agent_list).id
            })
            staff_list.append(staff_info)
        return staff_list

    def create(self, staff_info, result_mapping):
        staff_qs = Staff.query().filter(
            work_number = staff_info.work_number,
            agent_id = staff_info.agent_id
        )
        if staff_qs.count():
            staff = staff_qs[0]
        else:
            person_list = result_mapping.get(PersonGenerator.get_key())
            enterprise_list = result_mapping.get(EnterpriseGenerator.get_key())
            for person in person_list:
                for enterprise in enterprise_list:
                    staff = Staff.create(
                        company_id = enterprise.id,
                        person_id = person.id,
                        **staff_info
                    )
        return staff

    def delete(self):
        print('======================>>> delete staff <======================')
        return None
