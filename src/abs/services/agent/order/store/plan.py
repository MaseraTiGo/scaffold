# coding=UTF-8

from abs.common.model import BaseModel, IntegerField, CharField, DateTimeField, timezone, \
        ForeignKey, CASCADE
from abs.services.agent.order.settings import DB_PREFIX
from abs.services.agent.order.utils.constant import PlanStatus
from abs.services.agent.order.store.order import Order


class Plan(BaseModel):
    order = ForeignKey(Order, on_delete = CASCADE)
    number = CharField(verbose_name = "回款单号", max_length = 24, default = '')
    payment_record_id = IntegerField(verbose_name = "订单支付单id", default = 0)
    staff_id = IntegerField(verbose_name = "员工id", default = 0)
    plan_time = DateTimeField(verbose_name = "计划回款时间", null = True)
    plan_amount = IntegerField(verbose_name = "计划回款金额", default = 0)
    status = CharField(
        verbose_name = "状态",
        max_length = 64,
        choices = PlanStatus.CHOICES,
        default = PlanStatus.WAIT_PAY
    )

    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)

    class Meta:
        db_table = DB_PREFIX + "plan"

    @classmethod
    def search(cls, **attrs):
        plan_qs = cls.query().filter(**attrs)
        return plan_qs
