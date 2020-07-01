# coding=UTF-8

from support.generator.helper import *
from support.simulate.data.base import BaseMaker

from support.simulate.tool.template.staff import StaffTemplate


class StaffMaker(BaseMaker):

    def generate_relate(self, staff_generator, account_generator):
        staff_generator.add_outputs(account_generator)
        # access_generator.add_inputs(staff_generator, role_generator, department_generator)
        return staff_generator

    def generate(self):
        staff = StaffGenerator(StaffTemplate().generate())
        account = StaffAccountGenerator()
        # department = DepartmentGenerator(DepartmentTemplate().generate())
        # role = RoleGenerator(RoleTemplate().generate())
        # auth = AuthAccessGenerator()
        staff_generator = self.generate_relate(staff, account)
        staff_generator.generate()
        return staff_generator
