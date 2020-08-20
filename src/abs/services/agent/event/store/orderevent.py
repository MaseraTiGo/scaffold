# coding=UTF-8

from abs.common.model import BaseModel, BooleanField, \
        IntegerField, CharField, TextField, DateTimeField, timezone
from abs.services.agent.event.settings import DB_PREFIX
from abs.services.agent.event.store.eventbase import EventBase


class StaffOrderEvent(EventBase):
    order_id = IntegerField(verbose_name="订单id")

    class Meta:
        db_table = DB_PREFIX + "staff_order"
