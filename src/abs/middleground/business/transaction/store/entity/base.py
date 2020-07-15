# coding=UTF-8

'''
Created on 2020年7月10日

@author: Administrator
'''

from abs.common.model import BaseModel, ForeignKey, CASCADE, \
        IntegerField, TextField, CharField, DateTimeField, timezone
from abs.middleground.business.transaction.utils.constant import PayTypes,\
        BusinessTypes, TransactionStatus, OwnTypes
from abs.middleground.business.transaction.settings import DB_PREFIX


class BaseTransaction(BaseModel):
    """
    交易基类
    """
    number = CharField(verbose_name="交易编号", max_length=48)
    amount = IntegerField(verbose_name="金额，有正负之分, 单位：分")
    remark = TextField(verbose_name="记录备注", default="")

    pay_type = CharField(
        verbose_name="支付方式",
        max_length=12,
        choices=PayTypes.CHOICES
    )
    business_type = CharField(
        verbose_name="业务来源",
        max_length=16,
        choices=BusinessTypes.CHOICES
    )
    # 需要确认来源凭证ID，进出账都可以：包含余额id，订单id，红包id等
    business_id = IntegerField(verbose_name="业务ID", null=True)

    own_type = CharField(
        verbose_name="拥有者类型",
        max_length=16,
        choices=OwnTypes.CHOICES
    )
    own_id = IntegerField(verbose_name="拥有者ID")
    trader_type = CharField(
        verbose_name="交易者类型",
        max_length=16,
        choices=OwnTypes.CHOICES
    )
    trader_id = IntegerField(verbose_name="交易者ID", null=True)

    class Meta:
        abstract = True


class TransactionRecord(BaseTransaction):
    """
    客户交易记录
    """
    input_record_id = IntegerField(verbose_name="入账单ID", null=True)
    output_record_id = IntegerField(verbose_name="出账单ID", null=True)
    create_time = DateTimeField(verbose_name="创建时间", default=timezone.now)

    class Meta:
        db_table = DB_PREFIX + "record"

    @classmethod
    def generate_number(cls):
        import time
        return "TR" + str(int(time.time()))

    @classmethod
    def search(cls, **attrs):
        transaction_qs = cls.query().filter(**attrs).order_by('-create_time')
        return transaction_qs

    @classmethod
    def create(cls, **transacation_record):
        transacation_record.update({"number": cls.generate_number()})
        return super(TransactionRecord, cls).create(**transacation_record)


class TransactionInputRecord(BaseTransaction):
    """
    客户入账记录
    """
    status = CharField(
        verbose_name="交易状态",
        max_length=24,
        choices=TransactionStatus.CHOICES,
        default=TransactionStatus.PAY_FINISH
    )

    transaction = ForeignKey(TransactionRecord, null=True, on_delete=CASCADE)
    update_time = DateTimeField(verbose_name="更新时间", auto_now=True)
    create_time = DateTimeField(verbose_name="创建时间", default=timezone.now)

    class Meta:
        db_table = DB_PREFIX + "input_record"

    @classmethod
    def generate_number(cls):
        import time
        return "TRI" + str(int(time.time()))

    @classmethod
    def create(cls, **input_infos):
        input_infos.update({"number": cls.generate_number()})
        input_record = super(TransactionInputRecord, cls).create(**input_infos)
        return input_record

    def update(self, **output_infos):
        self = super(TransactionInputRecord, self).update(**output_infos)
        if self.status == TransactionStatus.ACCOUNT_FINISH \
           and self.transaction is None:
            transacation_record = TransactionRecord.create(
                amount=self.amount,
                pay_type=self.pay_type,
                remark=self.remark,
                input_record_id=self.id,
                business_type=self.business_type,
                business_id=self.business_id,
                own_type=self.own_type,
                own_id=self.own_id,
                trader_type=self.trader_type,
                trader_id=self.trader_id,
                create_time=self.create_time,
            )
            self.update(transaction=transacation_record)
        return self

    @classmethod
    def search(cls, **attrs):
        bankcard_qs = cls.query().filter(**attrs)
        return bankcard_qs


class TransactionOutputRecord(BaseTransaction):
    """
    客户出账记录
    """
    status = CharField(
        verbose_name="交易状态",
        max_length=24,
        choices=TransactionStatus.CHOICES,
        default=TransactionStatus.PAY_FINISH
    )

    transaction = ForeignKey(TransactionRecord, null=True, on_delete=CASCADE)
    update_time = DateTimeField(verbose_name="更新时间", auto_now=True)
    create_time = DateTimeField(verbose_name="创建时间", default=timezone.now)

    class Meta:
        db_table = DB_PREFIX + "output_record"

    @classmethod
    def generate_number(cls):
        import time
        return "TRO" + str(int(time.time()))

    @classmethod
    def search(cls, **attrs):
        bankcard_qs = cls.query().filter(**attrs)
        return bankcard_qs

    @classmethod
    def create(cls, **output_infos):
        output_infos.update({"number": cls.generate_number()})
        output_record = super(TransactionOutputRecord, cls).create(
            **output_infos
        )
        if output_record:
            transacation_record = TransactionRecord.create(
                amount=output_record.amount,
                pay_type=output_record.pay_type,
                remark=output_record.remark,
                output_record_id=output_record.id,
                business_type=output_record.business_type,
                business_id=output_record.business_id,
                own_type=output_record.own_type,
                own_id=output_record.own_id,
                trader_type=output_record.trader_type,
                trader_id=output_record.trader_id,
                create_time=output_record.create_time,
            )
            output_record.update(transaction=transacation_record)
        return output_record
