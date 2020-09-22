# coding=UTF-8

from abs.common.model import BaseModel, BooleanField, \
        IntegerField, CharField, TextField, DateTimeField, timezone, \
        ForeignKey, CASCADE
from abs.middleground.business.person.assistor.staff.model import \
        AbstractStaff
from abs.services.crm.staff.settings import DB_PREFIX
from abs.services.crm.staff.store import Company


class Staff(AbstractStaff):
    company = ForeignKey(Company, on_delete = CASCADE, null = True)
    name = CharField(verbose_name = "姓名", max_length = 32, default = "")
    phone = CharField(verbose_name = "手机号", max_length = 20, default = "")


    class Meta:
        db_table = DB_PREFIX + "base"

    @classmethod
    def search(cls, **attrs):
        staff_qs = cls.query().filter(**attrs)
        return staff_qs
