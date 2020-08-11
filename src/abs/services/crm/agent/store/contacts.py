# coding=UTF-8

from abs.common.model import BaseModel, BooleanField, \
        IntegerField, CharField, TextField, DateTimeField, timezone, \
        ForeignKey, CASCADE
from abs.middleground.business.person.utils.constant import GenderTypes
from abs.middleground.business.account.utils.constant import StatusTypes
from abs.services.crm.agent.settings import DB_PREFIX
from abs.services.crm.agent.store import Agent


class Contacts(BaseModel):
    agent = ForeignKey(Agent, on_delete=CASCADE)
    contacts = CharField(verbose_name="联系人", max_length=32, default="")
    phone = CharField(verbose_name="联系电话", max_length=16, default="")
    email = CharField(verbose_name="emali", max_length=64, default="")
    gender = CharField(
        verbose_name="性别",
        max_length=24,
        choices=GenderTypes.CHOICES,
        default=GenderTypes.UNKNOWN
    )
    account = CharField(verbose_name="账号", max_length=32, default="")

    update_time = DateTimeField(verbose_name="更新时间", auto_now=True)
    create_time = DateTimeField(verbose_name="创建时间", default=timezone.now)

    class Meta:
        db_table = DB_PREFIX + "contacts"

    @classmethod
    def search(cls, **attrs):
        contacts_qs = cls.query().filter(**attrs)
        return contacts_qs
