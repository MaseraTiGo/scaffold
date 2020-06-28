# coding=UTF-8


import hashlib
from django.db.models import Q

from infrastructure.core.exception.business_error import BusinessError
from infrastructure.utils.common.split_page import Splitor

from abs.service.base import BaseServer
from abs.middleware.token import TokenManager
from model.store.model_staff import Staff, Role, Department, DepartmentRole, Account


class StaffServer(BaseServer):

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


class StaffAccountServer(BaseServer):

    @classmethod
    def login(cls, username, password):
        is_exsited, account = Account.is_exsited(username, password)
        if is_exsited:
            token = TokenManager.generate_token('crm', account.staff.id)
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
