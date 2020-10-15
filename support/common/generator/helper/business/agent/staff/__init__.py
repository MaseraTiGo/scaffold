# coding=UTF-8

import random

from abs.services.agent.agent.models import Staff
from support.common.generator.base import BaseGenerator
from support.common.generator.helper import PersonGenerator, AgentGenerator


class AgentStaffGenerator(BaseGenerator):

    def __init__(self, staff_info):
        super(AgentStaffGenerator, self).__init__()
        self._staff_infos = self.init(staff_info)

    def get_create_list(self, result_mapping):
        staff_list = []
        for staff_info in self._staff_infos:
            staff_info.update({
            })
            staff_list.append(staff_info)
        return staff_list

    def create(self, staff_info, result_mapping):
        staff_qs = Staff.query().filter(
            work_number=staff_info.work_number,
        )
        if staff_qs.count():
            staff = staff_qs[0]
        else:
            person_list = result_mapping.get(PersonGenerator.get_key())
            agent_list = result_mapping.get(AgentGenerator.get_key())
            for person in person_list:
                if person.phone == staff_info.get('phone'):
                    staff_info.update({
                        'company': random.choice(agent_list),
                        'person_id': person.id,
                    })
                    staff = Staff.create(
                        **staff_info
                    )
        return staff

    def delete(self):
        print('======================>>> delete staff <======================')
        return None
