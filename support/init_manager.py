# coding=UTF-8

import init_envt

from infrastructure.utils.common.single import Single
from support.generator.helper import *
from support.init.loader import *


class InitManager(Single):

    def __init__(self):
        # staff init
        self._staff = StaffGenerator(StaffLoader().load())
        self._account = AccountGenerator()
        # self._department = DepartmentGenerator(DepartmentLoader().load())
        # self._role = RoleGenerator(RoleLoader().load())
        # self._access = DepartmentRoleGenerator()

    def generate_staff_relate(self):
        self._staff.add_outputs(self._account)
        # self._access.add_inputs(self._staff, self._role, self._department)
        return self._staff

    def run(self):
        staff_generator = self.generate_staff_relate()
        staff_generator.generate()


if __name__ == "__main__":
    InitManager().run()
