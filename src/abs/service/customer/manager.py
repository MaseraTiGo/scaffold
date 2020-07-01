# coding=UTF-8


import hashlib
from django.db.models import Q

from infrastructure.core.exception.business_error import BusinessError
from infrastructure.utils.common.split_page import Splitor

from abs.service.base import BaseServer
from abs.middleware.token import TokenManager
from model.common.model_account_base import StatusTypes
from model.store.model_customer import Customer, CustomerAccount, CustomerAddress, CustomerBankCard


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
        customer = Customer.create(**customer_info)
        return customer

    @classmethod
    def update(cls, customer_id, **update_info):
        customer = cls.get_byid(customer_id)
        customer.update(**update_info)
        return customer

    @classmethod
    def add_address(cls, customer_id, **address_info):
        customer = cls.get_byid(customer_id)
        address = CustomerAddress.create(customer = customer, **address_info)
        return address

    @classmethod
    def get_address(cls, address_id):
        address = CustomerAddress.get_byid(address_id)
        return address

    @classmethod
    def get_all_address(cls, customer_id):
        address_qs = CustomerAddress.search(customer = customer_id)
        return address_qs
    
    @classmethod
    def remove_address(cls, address_id):
        return cls.get_address(address_id).delete()

    @classmethod
    def update_address(cls, address_id, **address_info):
        address = cls.get_address(address_id)
        address.update(**address_info)
        return address

    @classmethod
    def add_bankcard(cls, customer_id, bank_number, **bankcard_info):
        customer = cls.get_byid(customer_id)

        # todo: add card to verify
        bank_name, bank_code = '中国工商银行', 'ICBC'

        bankcard = CustomerBankCard.create(customer = customer, bank_name = bank_name, bank_code =
                                           bank_code, bank_number = bank_number, **bankcard_info)
        return bankcard

    @classmethod
    def get_bankcard(cls, bankcard_id):
        bankcard = CustomerBankCard.get_byid(bankcard_id)
        return bankcard

    @classmethod
    def get_all_bankcard(cls, customer_id):
        bankcard = CustomerBankCard.search(customer = customer_id)
        return bankcard

    @classmethod
    def remove_bankcard(cls, bankcard_id):
        return cls.get_bankcard(bankcard_id).delete()


class CustomerAccountServer(BaseServer):

    @classmethod
    def register(cls, phone, password, code):
        customer_qs = Customer.search(phone = phone)
        customer_account_qs = CustomerAccount.search(username = phone)
        if customer_qs.count() > 0 or customer_account_qs.count() > 0:
            raise BusinessError('账号或密码已存在！')

        customer = Customer.create(phone = phone)
        customer_account = CustomerAccount.create(customer = customer, username = phone, \
                                                  password = password, status = StatusTypes.ENABLE)
        token = TokenManager.generate_token('user', customer.id)
        return token

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
