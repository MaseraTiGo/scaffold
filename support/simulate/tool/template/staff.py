# coding=UTF-8

from support.generator.field.normal import *
from support.generator.field.model import *

from support.simulate.tool.template.base import BaseTemplate


class StaffTemplate(BaseTemplate):

    def generate(self):
        birthday  = DateHelper().generate(years = 30)
        entry_time = DateHelper().generate(years = 4)
        expire_time = DateHelper().generate(years = 2)
        if entry_time > expire_time:
            entry_time, expire_time = expire_time, entry_time

        return {
            'identification': IdentificationHelper().generate(),
            'name': NameHelper().generate(),
            'gender': GenderConstant().generate(),
            'birthday': birthday,
            'id_number': WorkNumberHelper().generate(),
            'phone': PhoneHelper().generate(),
            'email': EmailHelper().generate(),
            'entry_time':entry_time,
            'education': EducationConstant().generate(),
            'is_admin': False,
        }
