# coding=UTF-8


from infrastructure.core.exception.business_error import BusinessError

from abs.middleware.token import TokenManager
from abs.middleground.business.account.utils.constant import StatusTypes
from abs.services.crm.account.models import StaffAccount


class StaffAccountServer(object):

    ACCOUNT_CLS = StaffAccount

    FLAG = "crm"

    @classmethod
    def create(cls, staff_id, username, password):
        account_qs = cls.ACCOUNT_CLS.search(staff_id=staff_id)
        if account_qs.count() > 0:
            raise BusinessError('客户已存在，不能创建账号！')

        account = cls.ACCOUNT_CLS.create(
            staff_id=staff_id,
            username=username,
            password=password,
            status=StatusTypes.ENABLE
        )
        token = TokenManager.generate_token(cls.FLAG, account.staff_id)
        return token

    @classmethod
    def renew_token(cls, auth_str, renew_str):
        return TokenManager.renew_token(auth_str, renew_str)

    @classmethod
    def login(cls, username, password):
        is_exsited, account = cls.ACCOUNT_CLS.is_exsited(username, password)
        if is_exsited:
            token = TokenManager.generate_token(cls.FLAG, account.staff_id)
            return token
        raise BusinessError('账号或密码不存在！')

    @classmethod
    def is_exsited(cls, username):
        account = cls.ACCOUNT_CLS.get_byusername(username)
        if account is None:
            return False
        return True

    @classmethod
    def modify_password(cls, staff_id, old_password, new_password):
        account = cls.ACCOUNT_CLS.get_bystaff(staff_id)
        if account.password != old_password:
            raise BusinessError('老密码不正确，请重试！')
        account.update(password=new_password)
        return True

    @classmethod
    def forget_password(cls, phone, code, new_password):
        # todo: 需要获取验证码
        if code != "123456":
            raise BusinessError('验证码错误，请重新输入！')
        account = cls.ACCOUNT_CLS.get_byusername(phone)
        if account is None:
            raise BusinessError('账户不存在！')

        account.update(password=new_password)
        token = TokenManager.generate_token(cls.FLAG, account.staff_id)
        return token

    @classmethod
    def logout(cls, staff_id):
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
