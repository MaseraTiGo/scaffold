# coding=UTF-8

from abs.common.model import BaseModel, \
        IntegerField, CharField, DateTimeField, timezone
from abs.services.customer.personal.settings import DB_PREFIX


class Customer(BaseModel):
    nick = CharField(verbose_name="昵称", max_length=32)
    head_url = CharField(verbose_name="头像URL", max_length=256, default="")

    person_id = IntegerField(verbose_name="用户id")

    update_time = DateTimeField(verbose_name="更新时间", auto_now=True)
    create_time = DateTimeField(verbose_name="创建时间", default=timezone.now)

    class Meta:
        db_table = DB_PREFIX + "base"

    @classmethod
    def search(cls, **attrs):
        customer_qs = cls.query().filter(**attrs)
        return customer_qs
