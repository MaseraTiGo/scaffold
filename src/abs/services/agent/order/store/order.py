# coding=UTF-8

from abs.common.model import BaseModel, IntegerField, CharField, DateTimeField, timezone
from abs.services.agent.order.settings import DB_PREFIX
from abs.services.agent.order.utils.constant import OrderSource
from abs.middleground.business.order.utils.constant import OrderStatus
from abs.middleground.business.transaction.utils.constant import PayTypes, \
        PayService

class Order(BaseModel):
    agent_customer_id = IntegerField(verbose_name = "代理商客户id", default = 0)
    mg_order_id = IntegerField(verbose_name = "订单id")
    agent_id = IntegerField(verbose_name = "代理商id", default = 0)
    person_id = IntegerField(verbose_name = "用户id", default = 0)
    company_id = IntegerField(verbose_name = "公司id", default = 0)
    pay_services = CharField(
        verbose_name = "订单支付服务",
        max_length = 128,
        choices = PayService.CHOICES,
        default = PayService.FULL_PAYMENT
    )
    source = CharField(
        verbose_name = "订单来源",
        max_length = 64,
        choices = OrderSource.CHOICES,
        default = OrderSource.OTHER
    )

    number = CharField(verbose_name = "订单编号", max_length = 24, default = '')
    status = CharField(
        verbose_name = "订单状态",
        max_length = 24,
        choices = OrderStatus.CHOICES,
        default = OrderStatus.ORDER_LAUNCHED
    )
    last_payment_time = DateTimeField(
        verbose_name = "最后支付时间",
        null = True,
        default = None,
    )
    name = CharField(verbose_name = "姓名", max_length = 16, default = "")
    phone = CharField(verbose_name = "手机号", max_length = 24, default = "")

    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)

    class Meta:
        db_table = DB_PREFIX + "base"

    @classmethod
    def search(cls, **attrs):
        order_qs = cls.query().filter(**attrs)
        return order_qs
