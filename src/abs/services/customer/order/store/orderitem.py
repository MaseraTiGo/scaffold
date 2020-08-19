# coding=UTF-8

from abs.common.model import BaseModel, BooleanField, \
        IntegerField, CharField, TextField, DateTimeField, timezone, \
        ForeignKey, CASCADE
from abs.services.agent.goods.utils.constant import DurationTypes, CategoryTypes
from abs.services.customer.order.settings import DB_PREFIX
from abs.services.customer.order.store.order import Order


class OrderItem(BaseModel):
    order = ForeignKey(Order, on_delete=CASCADE)
    goods_id = IntegerField(verbose_name="商品id")
    merchandise_snapshoot_id = IntegerField(verbose_name="商品快照id")

    school_name = CharField(verbose_name="学校名称", max_length=32, default="")
    school_city = CharField(verbose_name="学校城市", max_length=32, default='')
    major_name = CharField(verbose_name="专业名称", max_length=64, default="")
    category = CharField(
        verbose_name="类别",
        max_length=64,
        choices=CategoryTypes.CHOICES,
        default=CategoryTypes.OTHER
    )
    duration = CharField(
        verbose_name="时长",
        max_length=32,
        choices=DurationTypes.CHOICES,
        default=DurationTypes.OTHER
    )

    update_time = DateTimeField(verbose_name="更新时间", auto_now=True)
    create_time = DateTimeField(verbose_name="创建时间", default=timezone.now)

    class Meta:
        db_table = DB_PREFIX + "orderitem"

    @classmethod
    def search(cls, **attrs):
        orderitem_qs = cls.query().filter(**attrs)
        return orderitem_qs
