# coding=UTF-8

from support.simulate.tool.base.general import *
from support.simulate.tool.base.model import GenderHelper, RoleHelper, DepartmentHelper
from support.simulate.tool.template.base import BaseTemplate


class StaffTemplate(BaseTemplate):

    def generate(self):
        bank_name, bank_number = BankCardHelper().generate()
        contract = ContractHelper().generate()
        birthday  = DateHelper().generate(years = 30)
        create_time = DateTimeHelper().generate(years = 2)
        entry_time = DateHelper().generate(years = 4)
        expire_time = DateHelper().generate(years = 2)
        if entry_time > expire_time:
            entry_time, expire_time = expire_time, entry_time

        return {
            'identity': IdentityHelper().generate(),
            'name': NameHelper().generate(),
            'gender': GenderHelper().generate(),
            'birthday': birthday ,
            'phone': PhoneHelper().generate(),
            'email': EmailHelper().generate(),
            'city': CityHelper().generate(),
            'address': AddressHelper().generate(),
            'number': NumberHelper().generate(),
            'emergency_contact': NameHelper().generate(),
            'emergency_phone': PhoneHelper().generate(),
            'entry_time': entry_time,
            'education': EducationHelper().generate(),
            'bank_number': bank_number,
            'bank_name': bank_name,
            'contract_b': contract + 'b',
            'contract_l': contract + 'l',
            'expire_time': expire_time,
            'is_working': True,
            'is_admin': True,
            'create_time': create_time,
        }


class DepartmentTemplate(BaseTemplate):

    def generate(self):
        department = DepartmentHelper().generate()
        return {
            'name': department.name,
            'parent': department.parent.name,
            'describe': department.describe,
        }


class RoleTemplate(BaseTemplate):

    def generate(self):
        role = RoleHelper().generate()
        return {
            'name': role.name,
            'parent': role.parent.name,
            'describe': role.describe,
            'is_show_data': True,
        }
