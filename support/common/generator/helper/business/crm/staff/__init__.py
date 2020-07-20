# coding=UTF-8

import random

from support.common.generator.base import BaseGenerator
from support.common.generator.helper import EnterpriseGenerator
from abs.middleground.business.person.models import Person,\
        PersonStatus, PersonStatistics
from abs.services.crm.staff.models import Staff


class StaffGenerator(BaseGenerator):

    def __init__(self, staff_info):
        super(StaffGenerator, self).__init__()
        self._staff_infos = self.init(staff_info)

    def get_create_list(self, result_mapping):
        return self._staff_infos

    def create(self, staff_info, result_mapping):
        staff_qs = Staff.query().filter(work_number=staff_info.work_number)
        if staff_qs.count():
            staff = staff_qs[0]
        else:
            is_exsitd, person = Person.is_exsited(staff_info.phone)
            if not is_exsitd:
                person = Person.create(**staff_info)
                PersonStatus.create(person=person)
                PersonStatistics.create(person=person)

            enterprise_list = result_mapping.get(EnterpriseGenerator.get_key())
            enterprise = random.choice(enterprise_list)
            staff = Staff.create(
                company_id=enterprise.id,
                person_id=person.id,
                **staff_info
            )
        return staff

    def delete(self):
        print('======================>>> delete staff <======================')
        return None
