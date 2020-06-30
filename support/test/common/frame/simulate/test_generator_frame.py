# coding=UTF-8

import unittest
import json

from support.generator.helper.account import AccountGenerator
from support.generator.helper.department import DepartmentGenerator
from support.generator.helper.role import RoleGenerator
from support.generator.helper.rule import RuleGenerator
from support.generator.helper.staff import StaffGenerator


class TestGenerator(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_generator_graph(self):
        """test generator graph"""
        staff = StaffGenerator()
        account = AccountGenerator()
        department = DepartmentGenerator()
        role = RoleGenerator()
        rule = RuleGenerator()

        staff.add_outputs(role, department, account)
        role.add_outputs(rule)

        ponit_list = [staff, account, department, role, rule]
        for ponit in ponit_list:
            print('>>>>>>>>>>>>' * 5)
            ponit.generate()
            print('============' * 5)
            ponit.clear()
            print('<<<<<<<<<<<<'  * 5)
            print("")
