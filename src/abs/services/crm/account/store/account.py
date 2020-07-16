# coding=UTF-8

from abs.common.model import IntegerField
from abs.services.crm.account.settings import DB_PREFIX
from abs.middleground.business.account.store.abstract import BaseAccount


class StaffAccount(BaseAccount):
    """
    员工账号表
    """
    staff_id = IntegerField(verbose_name="客户id")

    class Meta:
        db_table = DB_PREFIX + "base"

    @classmethod
    def get_bystaff(cls, staff_id):
        try:
            return cls.objects.filter(staff_id=staff_id)[0]
        except Exception as e:
            return None

    @classmethod
    def get_byusername(cls, username):
        try:
            return cls.objects.filter(username=username)[0]
        except Exception as e:
            return None
