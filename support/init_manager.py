# coding=UTF-8

import init_envt

from infrastructure.utils.common.single import Single
from support.generator.helper import *
from support.init.loader import *


class InitManager(Single):

    def __init__(self):
        # staff init
        self._enterprise = EnterpriseGenerator(EnterpriseLoader().load())
        self._staff = StaffGenerator(StaffLoader().load())
        self._staff_account = StaffAccountGenerator()
        # self._department = DepartmentGenerator(DepartmentLoader().load())
        # self._role = RoleGenerator(RoleLoader().load())
        # self._access = DepartmentRoleGenerator()

        # customer init 
        self._customer = CustomerGenerator(CustomerLoader().load())
        self._customer_account = CustomerAccountGenerator()


    def generate_staff_relate(self):
        self._staff.add_outputs(self._staff_account)
        self._staff.add_inputs(self._enterprise)
        # self._access.add_inputs(self._staff, self._role, self._department)

        self._customer.add_outputs(self._customer_account)
        return self._enterprise, self._customer

    def run(self):
        enterprise_generator, customer_generator = self.generate_staff_relate()
        enterprise_generator.generate()
        customer_generator.generate()


if __name__ == "__main__":
    InitManager().run()
