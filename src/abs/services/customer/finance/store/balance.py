# coding=UTF-8

from abs.common.model import BaseModel, Sum, \
        IntegerField, CharField, TextField, DateTimeField, timezone
from abs.middleground.business.transaction.utils.constant import PayTypes
from abs.services.customer.finance.settings import DB_PREFIX


class CustomerBalanceRecord(BaseModel):
    """
    客户余额记录
    """
    number = CharField(verbose_name="交易编号", max_length=48)
    amount = IntegerField(verbose_name="金额，有正负之分，单位：分")
    pay_type = CharField(
        verbose_name="支付方式",
        max_length=12,
        choices=PayTypes.CHOICES
    )
    remark = TextField(verbose_name="记录备注", default="")

    input_record_id = IntegerField(verbose_name="入账凭证id", null=True)
    output_record_id = IntegerField(verbose_name="出账凭证id", null=True)

    customer_id = IntegerField(verbose_name="客户id")

    update_time = DateTimeField(verbose_name="更新时间", auto_now=True)
    create_time = DateTimeField(verbose_name="创建时间", default=timezone.now)

    class Meta:
        db_table = DB_PREFIX + "balance"

    @classmethod
    def generate_number(cls):
        import time
        return "BL" + str(int(time.time()))

    @classmethod
    def create(cls, **transacation_record):
        transacation_record.update({
            "number": cls.generate_number(),
        })
        return super(CustomerBalanceRecord, cls).create(**transacation_record)

    @classmethod
    def search(cls, **attrs):
        bankcard_qs = cls.query().filter(**attrs)
        return bankcard_qs
