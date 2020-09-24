# coding=UTF-8
from abs.common.model import CharField
from abs.services.customer.account.settings import DB_PREFIX
from abs.middleground.business.account.store.abstract import BaseAccount
from abs.middleground.business.account.utils.constant import PlatformTypes
from abs.services.customer.account.utils.constant import LoginSystem


class CustomerAccount(BaseAccount):
    """
    客户账号表
    """

    last_login_phone_unique = CharField(
        verbose_name = "最后一次登陆设备编码",
         max_length = 128,
         default = ""
    )
    last_login_phone_system = CharField(
        verbose_name = "最后一次登陆手机系统" ,
        max_length = 32,
        choices = LoginSystem.CHOICES,
        default = LoginSystem.OTHER,
    )

    class Meta:
        db_table = DB_PREFIX + "base"

    @classmethod
    def get_role_type(cls):
        return PlatformTypes.CUSTOMER
