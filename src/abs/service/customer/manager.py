# coding=UTF-8


import hashlib
from django.db.models import Q

from infrastructure.core.exception.business_error import BusinessError
from infrastructure.utils.common.split_page import Splitor

from abs.service.base import BaseServer
from abs.middleware.token import TokenManager
from model.store.model_customer import Customer, CustomerAccount


class CustomerServer(BaseServer):

    @classmethod
    def get(cls, customer):
        return cls.get_byid(customer.id)

    @classmethod
    def get_byid(cls, customer_id):
        customer = Customer.get_byid(customer_id)
        return customer

    @classmethod
    def search(cls, current_page, **search_info):
        customer_qs = Customer.search(**search_info)
        customer_qs.order_by('-create_time')
        return Splitor(current_page, customer_qs)

    @classmethod
    def generate(cls, customer_info):
        password = hashlib.md5('123456'.encode('utf8')).hexdigest()
        customer = Customer.create(**customer_info)
        return customer

    @classmethod
    def update(cls, customer_id, **update_info):
        customer = cls.get_byid(customer_id)
        customer.update(**update_info)
        return customer


class CustomerAccountServer(BaseServer):

    @classmethod
    def login(cls, username, password):
        is_exsited, account = CustomerAccount.is_exsited(username, password)
        if is_exsited:
            token = TokenManager.generate_token('user', account.customer.id)
            return token
        raise BusinessError('账号或密码不存在！')

    @classmethod
    def logout(cls, customer):
        pass

    @classmethod
    def get_phone_verification_code(cls, phone_number):
        return "123456"

    @classmethod
    def get_image_verification_code(cls):
        return "654321"
