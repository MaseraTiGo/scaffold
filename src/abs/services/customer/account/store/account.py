# coding=UTF-8

from abs.services.customer.account.settings import DB_PREFIX
from abs.middleground.business.account.store.abstract import BaseAccount
from abs.middleground.business.account.utils.constant import PlatformTypes


class CustomerAccount(BaseAccount):
    """
    客户账号表
    """

    class Meta:
        db_table = DB_PREFIX + "base"

    @classmethod
    def get_role_type(cls):
        return PlatformTypes.CUSTOMER
