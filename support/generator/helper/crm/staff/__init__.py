# coding=UTF-8

import random

from support.generator.base import BaseGenerator
from abs.middleground.business.person.models import Person
from support.generator.helper import EnterpriseGenerator
from abs.services.crm.staff.models import Staff


class StaffGenerator(BaseGenerator):

    def __init__(self, staff_info):
        super(StaffGenerator, self).__init__()
        self._staff_infos = self.init(staff_info)

    def get_create_list(self, result_mapping):
        enterprise_list = result_mapping.get(EnterpriseGenerator.get_key())
        for staff_info in self._staff_infos:
            enterprise = random.choice(enterprise_list)
            staff_info.company_id = enterprise.id

        return self._staff_infos

    def create(self, staff_info, result_mapping):
        staff_qs = Staff.query().filter(work_number=staff_info.work_number)
        if staff_qs.count():
            staff = staff_qs[0]
        else:
            is_exsitd, person = Person.is_exsited(staff_info.phone)
            if not is_exsitd:
                person = Person.create(**staff_info)

            staff = Staff.create(
                person_id=person.id,
                **staff_info
            )
        return staff

    def delete(self):
        print('======================>>> delete staff <======================')
        return None
