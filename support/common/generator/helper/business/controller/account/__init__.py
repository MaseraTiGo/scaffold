# coding=UTF-8

import hashlib
from infrastructure.utils.common.dictwrapper import DictWrapper
from support.common.generator.base import BaseGenerator
from support.common.generator.helper import ControllerStaffGenerator
from abs.middleground.business.account.utils.constant import StatusTypes,\
        PlatformTypes
from abs.middleground.business.person.models import Person
from abs.services.controller.account.models import StaffAccount


class ControllerStaffAccountGenerator(BaseGenerator):

    def get_create_list(self, result_mapping):
        staff_list = result_mapping.get(ControllerStaffGenerator.get_key())
        account_list = []
        for staff in staff_list:
            person = Person.get_byid(staff.person_id)
            if person.name == "yanfav5":
                username = person.name
            else:
                username = person.phone
            account_info = DictWrapper({
                "username": username,
                "password": hashlib.md5("123456".encode('utf8')).hexdigest(),
                "status": StatusTypes.ENABLE,
                "role_type": PlatformTypes.CRM,
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
