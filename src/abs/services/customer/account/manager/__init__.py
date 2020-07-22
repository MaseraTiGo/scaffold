# coding=UTF-8


from infrastructure.core.exception.business_error import BusinessError

from abs.common.manager import BaseManager
from abs.middleware.token import TokenManager
from abs.middleground.business.account.utils.constant import StatusTypes
from abs.services.customer.account.models import CustomerAccount


class CustomerAccountServer(BaseManager):

    ACCOUNT_CLS = CustomerAccount

    FLAG = "user"

    @classmethod
    def create(cls, customer_id, username, password):
        account_qs = cls.ACCOUNT_CLS.search(customer_id = customer_id)
        if account_qs.count() > 0:
            raise BusinessError('客户已存在，不能创建账号！')

        account = cls.ACCOUNT_CLS.create(
            customer_id = customer_id,
            username = username,
            password = password,
            status = StatusTypes.ENABLE
        )
        token = TokenManager.generate_token(cls.FLAG, account.customer_id)
        return token

    @classmethod
    def renew_token(cls, auth_str, renew_str):
        return TokenManager.renew_token(auth_str, renew_str)

    @classmethod
    def login(cls, username, password):
        is_exsited, account = cls.ACCOUNT_CLS.is_exsited(username, password)
        if is_exsited:
            token = TokenManager.generate_token(cls.FLAG, account.customer_id)
            return token
        raise BusinessError('账号或密码不存在！')

    @classmethod
    def is_exsited(cls, username):
        account = cls.ACCOUNT_CLS.get_byusername(username)
        if account is None:
            return False
        return True

    @classmethod
    def modify_password(cls, customer_id, old_password, new_password):
        account = cls.ACCOUNT_CLS.get_bycustomer(customer_id)
        if account.password != old_password:
            raise BusinessError('老密码不正确，请重试！')
        account.update(password = new_password)
        return True

    @classmethod
    def forget_password(cls, phone, code, new_password):
        # todo: 需要获取验证码
        if code != "123456":
            raise BusinessError('验证码错误，请重新输入！')
        account = cls.ACCOUNT_CLS.get_byusername(phone)
        if account is None:
            raise BusinessError('账户不存在！')

        account.update(password = new_password)
        token = TokenManager.generate_token(cls.FLAG, account.customer_id)
        return token

    @classmethod
    def logout(cls, customer_id):
        pass

    @classmethod
    def get_phone_verification_code(cls, phone_number):
        return "123456"

    @classmethod
    def check_phone_verification_code(cls, phone_number, code):
        if code != "123456":
            return False
        return True

    @classmethod
    def get_image_verification_code(cls):
        return "654321"

    @classmethod
    def check_image_verification_code(cls, phone_number, code):
        if code != "654321":
            return False
        return True

    @classmethod
    def hung_account(cls, customer_list):
        customer_mapping = {customer.id: customer for customer in customer_list}
        account_qs = cls.ACCOUNT_CLS.search(customer_id__in = customer_mapping.keys())
        for account in account_qs:
            customer_mapping[account.customer_id].account = None
            if account.customer_id in customer_mapping:
                customer_mapping[account.customer_id].account = account
        return customer_list
