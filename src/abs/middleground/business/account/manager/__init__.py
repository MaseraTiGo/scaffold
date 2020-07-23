# coding=UTF-8

from infrastructure.core.exception.business_error import BusinessError

from abs.common.manager import BaseManager
from abs.middleware.token import TokenManager
from abs.middleground.business.account.utils.constant import StatusTypes


class AccountServer(BaseManager):

    APPLY_CLS = None

    @classmethod
    def create(cls, role_id, username, password):
        account = cls.APPLY_CLS.get_byrole(role_id=role_id)
        if account is not None:
            raise BusinessError('客户已存在，不能创建账号！')

        account = cls.APPLY_CLS.create(
            role_id=role_id,
            username=username,
            password=password,
            status=StatusTypes.ENABLE
        )
        token = TokenManager.generate_token(
            account.role_type,
            account.role_id
        )
        return token

    @classmethod
    def renew_token(cls, auth_str, renew_str):
        return TokenManager.renew_token(auth_str, renew_str)

    @classmethod
    def login(cls, username, password):
        is_exsited, account = cls.APPLY_CLS.is_exsited(username, password)
        if is_exsited:
            token = TokenManager.generate_token(
                account.role_type,
                account.role_id
            )
            return token
        raise BusinessError('账号或密码不存在！')

    @classmethod
    def is_exsited(cls, username):
        account = cls.APPLY_CLS.get_byusername(username)
        if account is None:
            return False
        return True

    @classmethod
    def forget_password(cls, phone, code, new_password):
        # todo: 需要获取验证码
        if code != "123456":
            raise BusinessError('验证码错误，请重新输入！')
        account = cls.APPLY_CLS.get_byusername(phone)
        if account is None:
            raise BusinessError('账户不存在！')

        account.update(password=new_password)
        token = TokenManager.generate_token(
            account.role_type,
            account.role_id
        )
        return token

    @classmethod
    def modify_password(cls, role_id, old_password, new_password):
        account = cls.APPLY_CLS.get_byrole(role_id)
        if account.password != old_password:
            raise BusinessError('老密码不正确，请重试！')
        account.update(password=new_password)
        return True

    @classmethod
    def logout(cls, role_id):
        pass

    @classmethod
    def get_image_verification_code(cls):
        return "654321"

    @classmethod
    def check_image_verification_code(cls, phone_number, code):
        if code != "654321":
            return False
        return True
