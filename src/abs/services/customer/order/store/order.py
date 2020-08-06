# coding=UTF-8

from abs.common.model import BaseModel, IntegerField, CharField, DateTimeField, timezone
from abs.services.customer.order.settings import DB_PREFIX
from abs.services.customer.order.utils.constant import OrderSource


class Order(BaseModel):
    customer_id = IntegerField(verbose_name = "客户id")
    mg_order_id = IntegerField(verbose_name = "订单id")
    agent_id = IntegerField(verbose_name = "代理商id", null = True)

    source = CharField(
        verbose_name = "订单来源",
        max_length = 64,
        choices = OrderSource.CHOICES,
        default = OrderSource.OTHER
    )

    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)

    class Meta:
        db_table = DB_PREFIX + "base"

    @classmethod
    def search(cls, **attrs):
        order_qs = cls.query().filter(**attrs)
        return order_qs
