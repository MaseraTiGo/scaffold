# coding=UTF-8

from abs.common.model import BaseModel, BooleanField, \
        IntegerField, CharField, TextField, DateTimeField, \
        timezone, DateField, ForeignKey, CASCADE
from abs.services.agent.agent.settings import DB_PREFIX
from abs.middleground.business.person.assistor.staff.model import \
        AbstractStaff
from abs.services.agent.agent.store import Agent


class Staff(AbstractStaff):
    company = ForeignKey(Agent, on_delete = CASCADE)
    name = CharField(verbose_name = "姓名", max_length = 32, default = "")
    phone = CharField(verbose_name = "手机号", max_length = 20, default = "")

    class Meta:
        db_table = DB_PREFIX + "staff"

    @classmethod
    def search(cls, **attrs):
        staff_qs = cls.query().filter(**attrs)
        return staff_qs
