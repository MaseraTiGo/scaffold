# coding=UTF-8

'''
Created on 2020年7月10日

@author: Roy
'''

from abs.common.model import BaseModel, CASCADE, ForeignKey,\
        IntegerField, CharField, TextField, DateTimeField, timezone
from abs.middleground.business.order.settings import DB_PREFIX
from abs.middleground.business.transaction.utils.constant import OwnTypes
from abs.middleground.business.order.store.entity.requirement import \
        Requirement
from abs.middleground.business.order.store.entity.payment import Payment
from abs.middleground.business.order.store.entity.invoice import Invoice
from abs.middleground.business.order.utils.constant import OrderStatus


class Order(BaseModel):
    """
    订单
    """
    number = CharField(verbose_name="订单编号", max_length=24)
    description = TextField(verbose_name="订单描述", default="")
    remark = TextField(verbose_name="备注", default="")

    strike_price = IntegerField(verbose_name="成交金额，单位：分")
    requirement = ForeignKey(Requirement, on_delete=CASCADE)  # 需求单
    payment = ForeignKey(Payment, on_delete=CASCADE)  # 支付单
    invoice = ForeignKey(Invoice, on_delete=CASCADE)  # 发货单

    status = CharField(
        verbose_name="订单状态",
        max_length=24,
        choices=OrderStatus.CHOICES,
        default=OrderStatus.ORDER_LAUNCHED
    )

    launch_type = CharField(
        verbose_name="发起方类型",
        max_length=16,
        choices=OwnTypes.CHOICES
    )
    launch_id = IntegerField(verbose_name="发起方ID")
    server_type = CharField(
        verbose_name="服务方类型",
        max_length=16,
        choices=OwnTypes.CHOICES
    )
    server_id = IntegerField(verbose_name="服务方ID")
    update_time = DateTimeField(verbose_name="更新时间", auto_now=True)
    create_time = DateTimeField(verbose_name="创建时间", default=timezone.now)

    class Meta:
        db_table = DB_PREFIX + "order"

    @classmethod
    def generate_number(cls):
        import time
        return "OD" + str(time.time()).replace('.', '')

    @classmethod
    def create(cls, **order_info):
        order_info.update({
            "number": cls.generate_number(),
        })
        return super(Order, cls).create(**order_info)

    @classmethod
    def get_bypayment(cls, payment_id):
        order_qs = cls.query(
            payment_id=payment_id
        )
        if order_qs.count() > 0:
            return order_qs[0]
        return None
