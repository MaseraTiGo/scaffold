# coding=UTF-8

import hashlib
from infrastructure.utils.common.dictwrapper import DictWrapper
from support.common.generator.base import BaseGenerator
from support.common.generator.helper import AgentStaffGenerator
from abs.middleground.business.account.utils.constant import StatusTypes, \
        PlatformTypes
from abs.middleground.business.person.models import Person
from abs.services.agent.account.models import StaffAccount


class AgentStaffAccountGenerator(BaseGenerator):

    def get_create_list(self, result_mapping):
        staff_list = result_mapping.get(AgentStaffGenerator.get_key())
        account_list = []
        for staff in staff_list:
            person = Person.get_byid(staff.person_id)
            if person.name == "admin":
                username = person.name
            else:
                username = person.phone
            account_info = DictWrapper({
                "username": username,
                "password": hashlib.md5("123456".encode('utf8')).hexdigest(),
                "status": StatusTypes.ENABLE,
                "role_type": PlatformTypes.AGENT,
                "role_id": staff.id
            })
            account_list.append(account_info)
        return account_list

    def create(self, account_info, result_mapping):
        account = StaffAccount.get_byrole(account_info.role_id)
        if account is None:
            account = StaffAccount.create(**account_info)
        return account

    def delete(self):
        print('==================>>> delete account <======================')
        return None
