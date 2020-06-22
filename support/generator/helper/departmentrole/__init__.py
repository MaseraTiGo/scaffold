# coding=UTF-8

import random
from infrastructure.utils.common.dictwrapper import DictWrapper
from infrastructure.log.base import logger
from model.store.model_staff import DepartmentRole
from support.generator.base import BaseGenerator
from support.generator.helper.role import RoleGenerator
from support.generator.helper.department import DepartmentGenerator
from support.generator.helper.staff import StaffGenerator


class DepartmentRoleGenerator(BaseGenerator):

    def get_create_list(self, result_mapping):
        staff_list = result_mapping.get(StaffGenerator.get_key())
        role_list = result_mapping.get(RoleGenerator.get_key())
        department_list = result_mapping.get(DepartmentGenerator.get_key())

        department_role_list = []
        for staff in staff_list:
            if staff.id == 1:
                department = department_list[0]
                role = role_list[0]
            else:
                department = random.choice(department_list)
                role = random.choice(role_list)

            department_role = DictWrapper({})
            department_role.staff = staff
            department_role.department = department
            department_role.role = role

            department_role_list.append(department_role)

        return department_role_list

    def create(self, access, result_mapping):
        department_role_qs = DepartmentRole.query().filter(**access)
        if department_role_qs.count():
            department_role = department_role_qs[0]
        else:
            department_role = DepartmentRole.create(**access)
        return department_role

    def delete(self):
        print('======================>>> delete auth_access <======================')
        return None
