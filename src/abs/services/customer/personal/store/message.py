# coding=UTF-8

from abs.common.model import BaseModel, \
        IntegerField, CharField, DateTimeField, timezone, ForeignKey, CASCADE
from abs.services.customer.personal.settings import DB_PREFIX
from abs.services.customer.personal.store import Customer
from abs.services.customer.personal.utils.constant import MessageStatus


# todo: dong
class CustomerMessage(BaseModel):

    person = ForeignKey(Customer, on_delete=CASCADE, related_name='personal_messages')
    title = CharField(verbose_name="标题", max_length=64)
    content = CharField(verbose_name="内容", max_length=64)

    status = CharField(
        verbose_name="消息状态",
        max_length=32,
        choices=MessageStatus.CHOICES
    )

    update_time = DateTimeField(verbose_name="更新时间", auto_now=True)
    create_time = DateTimeField(verbose_name="创建时间", default=timezone.now)

    class Meta:
        db_table = DB_PREFIX + "message"

    @classmethod
    def search(cls, **attrs):
        customer_qs = cls.query().filter(**attrs)
        return customer_qs
