# coding=UTF-8


import hashlib
from django.db.models import Q

from infrastructure.core.exception.business_error import BusinessError
from infrastructure.utils.common.split_page import Splitor

from abs.service.staff.token import Token
from model.store.model_staff import Staff, Role, Department, DepartmentRole, Account


class StaffServer(object):

    @classmethod
    def get(cls, staff):
        return cls.get_byid(staff.id)

    @classmethod
    def get_byid(cls, staff_id):
        staff = Staff.get_byid(staff_id)
        return staff

    @classmethod
    def search(cls, current_page, **search_info):
        staff_qs = Staff.search(**search_info)
        staff_qs.order_by('-create_time')
        return Splitor(current_page, staff_qs)

    @classmethod
    def generate(cls, staff_info):
        password = hashlib.md5('123456'.encode('utf8')).hexdigest()
        staff = Staff.create(**staff_info)
        return staff

    @classmethod
    def update(cls, staff_id, **update_info):
        staff = cls.get_byid(staff_id)
        staff.update(**update_info)
        return staff


class StaffAccountServer(object):

    @classmethod
    def login(cls, username, password):
        is_exsited, account = Account.is_exsited(username, password)
        if is_exsited:
            token = StaffTokenServer.generate_token(account.staff)
            return token
        raise BusinessError('账号或密码不存在！')

    @classmethod
    def logout(cls, staff):
        pass

    @classmethod
    def get_phone_verification_code(cls, phone_number):
        return "123456"

    @classmethod
    def get_image_verification_code(cls):
        return "654321"

class StaffTokenServer(object):

    @classmethod
    def generate_token(cls, staff):
        token = Token.generate(staff.id, 'staff')
        return token

    @classmethod
    def renew_token(cls, auth_str, renew_str):
        token = Token.get(auth_str)
        token.renew(renew_str)
        return token

    @classmethod
    def get_token(cls, auth_str, parms = None):
        token = Token.get(auth_str)
        token.check(parms)
        return token
