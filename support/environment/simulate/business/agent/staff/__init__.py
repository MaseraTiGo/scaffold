# coding=UTF-8

from support.common.maker import BaseLoader
from support.common.generator.field.normal import *
from support.common.generator.field.model import *


class AgentStaffLoader(BaseLoader):

    def generate(self):
        birthday = DateHelper().generate(years=30)
        entry_time = DateHelper().generate(years=4)
        expire_time = DateHelper().generate(years=2)
        if entry_time > expire_time:
            entry_time, expire_time = expire_time, entry_time

        return {
            'name': NameHelper().generate(),
            'gender': GenderConstant().generate(),
            'birthday': birthday,
            'work_number': WorkNumberHelper().generate(),
            'phone': PhoneHelper().generate(),
            'email': EmailHelper().generate(),
            'is_admin': False,
        }
