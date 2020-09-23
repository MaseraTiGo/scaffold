# coding=UTF-8

from abs.common.model import BaseModel, BooleanField, \
        IntegerField, CharField, TextField, DateTimeField, timezone
from abs.middleground.business.enterprise.assistor.link.model import \
        AbstractCompany
from abs.services.agent.agent.settings import DB_PREFIX


class Agent(AbstractCompany):
    province = CharField(verbose_name = "省", max_length = 32, default = "")
    city = CharField(verbose_name = "市", max_length = 32, default = "")
    area = CharField(verbose_name = "区", max_length = 32, default = "")
    address = CharField(verbose_name = "详细地址", max_length = 128, default = "")
    official_seal = TextField(verbose_name = "公章", default = "")

    class Meta:
        db_table = DB_PREFIX + "base"

    @classmethod
    def search(cls, **attrs):
        agent_qs = cls.query().filter(**attrs)
        return agent_qs
