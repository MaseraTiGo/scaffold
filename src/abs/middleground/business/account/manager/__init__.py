# coding=UTF-8

import datetime
import hashlib

from infrastructure.core.exception.business_error import BusinessError
from abs.common.manager import BaseManager
from abs.middleware.token import TokenManager
from abs.middleground.business.account.utils.constant import StatusTypes


class AccountServer(BaseManager):
    """
    当前登录方式支持
    1. 账号密码登录
    """

    APPLY_CLS = None

    @classmethod
    def create(cls, role_id, username, password, ip=""):
        """
        创建账号接口
        """
        account = cls.APPLY_CLS.get_byrole(role_id=role_id)
        if account is not None:
            raise BusinessError('账号已存在，不能创建！')

        account = cls.APPLY_CLS.create(
            role_id=role_id,
            username=username,
            password=password,
            register_ip=ip,
            status=StatusTypes.ENABLE
        )
        token = TokenManager.generate_token(
            account.role_type,
            account.role_id
        )
        return token

    @classmethod
    def get(cls, role_id):
        """
        获取账号信息接口
        """
        account = cls.APPLY_CLS.get_byrole(role_id=role_id)
        if account is None:
            raise BusinessError('账号不存在')
        return account

    @classmethod
    def update(cls, role_id, **update_infos):
        """
        更新账号信息接口
        """
        account = cls.get(role_id)
        account.update(
            **update_infos
        )
        return account

    @classmethod
    def renew_token(cls, auth_str, renew_str):
        """
        续签访问令牌接口
        """
        return TokenManager.renew_token(auth_str, renew_str)

    @classmethod
    def login(cls, username, password, ip=""):
        """
        登录接口
        """
        is_exsited, account = cls.APPLY_CLS.is_exsited(username, password)
        if is_exsited:
            if account.status == StatusTypes.ENABLE:
                token = TokenManager.generate_token(
                    account.role_type,
                    account.role_id
                )
                account.update(
                    last_login_ip="",
                    last_login_time=datetime.datetime.now()
                )
                return token
            raise BusinessError('账号状态不可用！')
        raise BusinessError('账号或密码错误！')

    @classmethod
    def is_exsited(cls, username):
        """
        是否存在账号接口
        """
        account = cls.APPLY_CLS.get_byusername(username)
        if account is None:
            return False
        return True

    @classmethod
    def forget_password(cls, phone, code, new_password):
        """
        忘记密码接口
        """
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
        """
        修改密码接口
        """
        account = cls.APPLY_CLS.get_byrole(role_id)
        if account.password != old_password:
            raise BusinessError('原密码不正确，请重试！')
        account.update(password=new_password)
        return True

    @classmethod
    def logout(cls,  auth_str):
        """
        注销接口
        """
        TokenManager.clear_token(auth_str)
        return True

    @classmethod
    def get_byids(cls,  role_id_list, limit=100):
        """
        获取账号信息接口（通过角色id）
        """
        if len(role_id_list) > 100:
            raise BusinessError('账户搜索超过上限')
        account_qs = cls.APPLY_CLS.search(
            role_id__in=role_id_list
        )
        return account_qs
