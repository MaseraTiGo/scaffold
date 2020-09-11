# coding=UTF-8

'''
Created on 2020年7月10日

@author: Roy
'''

from abs.common.model import BaseModel, CASCADE,\
        IntegerField, CharField, DateTimeField, TextField,\
        ForeignKey, timezone
from abs.middleground.business.transaction.utils.constant import PayTypes,\
        PayService, TransactionStatus
from abs.middleground.business.order.settings import DB_PREFIX


class Payment(BaseModel):
    """
    订单支付单
    """
    actual_amount = IntegerField(verbose_name="实付金额，单位：分")
    """
    pay_services = CharField(
        verbose_name="订单支付服务",
        max_length=128,
        choices=PayService.CHOICES,
    )
    """
    last_payment_type = CharField(
        verbose_name="最后支付方式",
        max_length=16,
        choices=PayTypes.CHOICES,
        null=True,
        default=None,
    )
    last_payment_time = DateTimeField(
        verbose_name="最后支付时间",
        null=True,
        default=None,
    )
    last_payment_amount = IntegerField(verbose_name="最后支付金额", default=0)

    remark = TextField(verbose_name="备注", default="")
    update_time = DateTimeField(verbose_name="更新时间", auto_now=True)
    create_time = DateTimeField(verbose_name="创建时间", default=timezone.now)

    class Meta:
        db_table = DB_PREFIX + "payment"


class PaymentRecord(BaseModel):
    """
    订单支付记录信息
    """
    amount = IntegerField(verbose_name="实付金额，单位：分")
    pay_type = CharField(
        verbose_name="支付方式",
        max_length=16,
        choices=PayTypes.CHOICES,
        null=True,
        default=None,
    )
    status = CharField(
        verbose_name="交易状态",
        max_length=64,
        null=True,
        choices=TransactionStatus.CHOICES,
        default=TransactionStatus.PAY_REQUEST,
    )

    payment = ForeignKey(Payment, on_delete=CASCADE)
    output_record_id = IntegerField(verbose_name="出账凭证id", null=True)

    remark = TextField(verbose_name="备注", default="")
    update_time = DateTimeField(verbose_name="更新时间", auto_now=True)
    create_time = DateTimeField(verbose_name="创建时间", default=timezone.now)

    class Meta:
        db_table = DB_PREFIX + "payment_record"

    @classmethod
    def generate_number(cls):
        import time
        return "OPR" + str(time.time()).replace('.', '')

    @classmethod
    def get_byoutputrecord(cls, output_record_id):
        payment_qs = cls.query(output_record_id=output_record_id)
        if payment_qs.count():
            return payment_qs[0]
        return None
