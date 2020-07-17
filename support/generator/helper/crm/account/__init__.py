# coding=UTF-8

import hashlib
from infrastructure.utils.common.dictwrapper import DictWrapper
from support.generator.base import BaseGenerator
from support.generator.helper import StaffGenerator
from abs.middleground.business.account.utils.constant import StatusTypes
from abs.middleground.business.person.models import Person
from abs.services.crm.account.models import StaffAccount


class StaffAccountGenerator(BaseGenerator):

    def get_create_list(self, result_mapping):
        staff_list = result_mapping.get(StaffGenerator.get_key())
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
                "staff_id": staff.id
            })
            account_list.append(account_info)
        return account_list

    def create(self, account_info, result_mapping):
        account_qs = StaffAccount.query().filter(staff_id=account_info.staff_id)
        if account_qs.count():
            account = account_qs[0]
        else:
            account = StaffAccount.create(**account_info)
        return account

    def delete(self):
        print('==================>>> delete account <======================')
        return None
