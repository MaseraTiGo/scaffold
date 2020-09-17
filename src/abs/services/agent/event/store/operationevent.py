# coding=UTF-8

from abs.common.model import BaseModel, BooleanField, \
        IntegerField, CharField, TextField, DateTimeField, timezone
from abs.services.agent.event.settings import DB_PREFIX
from abs.services.agent.event.utils.constant import OperationTypes
from abs.services.agent.event.store.eventbase import EventBase


class OperationEvent(EventBase):
    agent_id = IntegerField(verbose_name = "代理商id")
    agent_customer_id = IntegerField(verbose_name = "代理商客户id", default = 0)
    describe = TextField(verbose_name = "描述")
    type = CharField(verbose_name = "跟中类型", \
                     max_length = 64, \
                     choices = OperationTypes.CHOICES, \
                     default = OperationTypes.OTHER)

    class Meta:
        db_table = DB_PREFIX + "operation"
