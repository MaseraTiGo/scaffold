# coding=UTF-8

from abs.common.model import BaseModel, BooleanField, \
        IntegerField, CharField, TextField, DateTimeField, timezone
from abs.services.agent.customer.settings import DB_PREFIX


class AgentCustomer(BaseModel):

    agent_id = IntegerField(verbose_name="agent_id")
    customer_id = IntegerField(verbose_name="customer_id")

    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)

    class Meta:
        db_table = DB_PREFIX + "base"

    @classmethod
    def search(cls, **attrs):
        agent_customer_qs = cls.query().filter(**attrs)
        return agent_customer_qs
