# coding=UTF-8

from abs.common.model import IntegerField
from abs.services.customer.account.settings import DB_PREFIX
from abs.middleground.business.account.store.abstract import BaseAccount


class CustomerAccount(BaseAccount):
    """
    客户账号表
    """
    customer_id = IntegerField(verbose_name="客户id")

    class Meta:
        db_table = DB_PREFIX + "account"

    @classmethod
    def get_bycustomer(cls, customer_id):
        try:
            return cls.objects.filter(customer_id=customer_id)[0]
        except Exception as e:
            return None

    @classmethod
    def get_byusername(cls, username):
        try:
            return cls.objects.filter(username=username)[0]
        except Exception as e:
            return None
