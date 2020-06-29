# coding=UTF-8

import hashlib
from infrastructure.log.base import logger
from infrastructure.utils.common.dictwrapper import DictWrapper
from support.generator.base import BaseGenerator
from support.generator.helper import StaffGenerator
from model.common.model_account_base import StatusTypes
from model.store.model_staff import StaffAccount


class AccountGenerator(BaseGenerator):

    def get_create_list(self, result_mapping):
        staff_list = result_mapping.get(StaffGenerator.get_key())
        account_list = []
        for staff in staff_list:
            if staff.name == "admin":
                username = staff.name
            else:
                username = staff.phone
            account_info = DictWrapper({
                "username": username,
                "password": hashlib.md5("123456".encode('utf8'))\
                                .hexdigest(),
                "status": StatusTypes.ENABLE,
                "staff": staff
            })
            account_list.append(account_info)
        return account_list

    def create(self, account_info, result_mapping):
        account_qs = StaffAccount.query().filter(staff = account_info.staff)
        if account_qs.count():
            account = account_qs[0]
        else:
            account = StaffAccount.create(**account_info)
        return account

    def delete(self):
        print('==================>>> delete account <======================')
        return None
