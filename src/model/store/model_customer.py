# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''
import json

from django.db.models import *
from django.utils import timezone
from model.base import BaseModel
from model.common.model_user_base import GenderTypes, EducationType, UserCertification
from model.common.model_account_base import BaseAccount


class Customer(BaseModel):
    """客户表"""
    name = CharField(verbose_name = "姓名", max_length = 32)
    gender = CharField(verbose_name = "性别", max_length = 24, choices = GenderTypes.CHOICES, default = GenderTypes.UNKNOWN)
    birthday = DateField(verbose_name = "生日", null = True, blank = True)
    education = CharField(verbose_name = "学历", max_length = 24, choices = EducationType.CHOICES, default = EducationType.OTHER)

    phone = CharField(verbose_name = "手机号", max_length = 20, default = "" , null = True)
    email = CharField(verbose_name = "邮箱", max_length = 128, default = "", null = True)
    wechat = CharField(verbose_name = "微信", max_length = 128, default = "", null = True)
    qq = CharField(verbose_name = "qq", max_length = 128, default = "", null = True)
    certification = ForeignKey(UserCertification, on_delete=DO_NOTHING, null = True, default = None)

    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)

    class Meta:
        db_table = "customer_info"

    @classmethod
    def get_customer_byname(cls, name):
        """根据姓名查询客户"""
        try:
            return cls.query().filter(name = name)[0]
        except:
            return None

    @classmethod
    def search(cls, **attrs):
        customer_qs = cls.query().filter(**attrs)
        return customer_qs

    """
    # todo: need to refractor
    def update(self, **infos):
        certification = None
        if self.certification:
            certification = self.certification.update(**infos)
        customer = super(Customer, self).update(certification = certification, **infos)
        return customer
    """

class CustomerAccount(BaseAccount):
    """客户账号表"""
    nick = CharField(verbose_name = "昵称", max_length = 64)
    profile = CharField(verbose_name = "头像", max_length = 256)
    customer = ForeignKey(Customer, on_delete=CASCADE)

    class Meta:
        db_table = "customer_account"

    @classmethod
    def search(cls, **attrs):
        account_qs = cls.query().filter(**attrs)
        return account_qs

    @classmethod
    def is_exsited(cls, username, password):
        account_qs = cls.objects.filter(username = username, password = password)
        if account_qs.count():
            return True, account_qs[0]
        return False, None

    @classmethod
    def get_byphone(cls, phone):
        customer_qs = Customer.search(phone = phone)
        if customer_qs.count() == 0:
            return None
        customer = customer_qs[0]

        account_qs = cls.query(customer = customer)
        if account_qs.count() == 0:
            return None
        account = account_qs[0]
        return account



    @classmethod
    def get_account_bycustomer(cls, customer_id):
        """根据customer_id查询账号信息"""
        try:
            return cls.objects.filter(customer = customer_id)[0]
        except:
            return None


class CustomerAddress(BaseModel):
    """客户联系地址"""
    contacts = CharField(verbose_name = "联系人", max_length = 64)
    gender = CharField(verbose_name = "性别", max_length = 24, choices = GenderTypes.CHOICES, default = GenderTypes.UNKNOWN)
    phone = CharField(verbose_name = "联系电话", max_length = 64)
    is_default = BooleanField(verbose_name = "是否默认", default= False)

    city = CharField(verbose_name = "城市", max_length = 64)
    address = CharField(verbose_name = "详细地址", max_length = 256)

    customer = ForeignKey(Customer, on_delete=CASCADE)

    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)

    class Meta:
        db_table = "customer_address"

    @classmethod
    def search(cls, **attrs):
        address_qs = cls.query().filter(**attrs)
        return address_qs


class CustomerBankCard(BaseModel):
    """客户银行卡"""
    bank_name = CharField(verbose_name = "银行名称", max_length = 24)
    bank_code = CharField(verbose_name = "银行编码", max_length = 20)
    bank_number = CharField(verbose_name = "银行卡号", max_length = 64)
    name = CharField(verbose_name = "开户人姓名", max_length = 16)
    phone = CharField(verbose_name = "开户人手机号", max_length = 20)
    identification = CharField(verbose_name = "开户人身份证", max_length = 24)

    customer = ForeignKey(Customer, on_delete=CASCADE)

    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)

    class Meta:
        db_table = "customer_bankcard"

    @classmethod
    def search(cls, **attrs):
        bankcard_qs = cls.query().filter(**attrs)
        return bankcard_qs


class AccountTypes(object):
    EXPEND = "expense"
    INCOME = "income"
    CHOICES = ((EXPEND, '支出'), (INCOME, "收入"))


class PayTypes(object):
    BANK = "bank"
    ALIPAY = "alipay"
    WECHAT = "wechat"
    BALANCE = "balance"
    CHOICES = ((BANK, '银行'), (ALIPAY, "支付宝"), (WECHAT, "微信"), (BALANCE, "余额"))


class BusinessTypes(object):
    ORDER = "order"
    BALANCE = "balance"
    CHOICES = ((ORDER, '订单'), (BALANCE, "余额"))


class TransactionStatus(object):
    PAY_FINISH = "pay_finish"
    TRANSACTION_DEALING = "transaction_dealing"
    ACCOUNT_FINISH = "account_finish"
    CHOICES = ((PAY_FINISH, '付款成功'), (TRANSACTION_DEALING, "交易处理中"), (ACCOUNT_FINISH, "到账成功"))


class CustomerTransactionRecord(BaseModel):
    """客户交易记录"""
    number = CharField(verbose_name = "交易编号", max_length = 48)
    amount = IntegerField(verbose_name = "金额，单位：分") # 有正负之分
    pay_type = CharField(verbose_name = "支付方式", max_length = 12, choices = PayTypes.CHOICES)
    remark = TextField(verbose_name = "记录备注", default = "")

    input_record_id = IntegerField(verbose_name = "入账单ID", null = True)
    output_record_id = IntegerField(verbose_name = "出账单ID", null = True)

    business_type = CharField(verbose_name = "业务来源", max_length = 16, choices = BusinessTypes.CHOICES)
    business_id = IntegerField(verbose_name = "业务ID", null = True) # 需要确认来源凭证ID，进出账都可以：包含余额id，订单id，红包id等

    customer = ForeignKey(Customer, on_delete=CASCADE)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)

    class Meta:
        db_table = "customer_transaction_record"

    @classmethod
    def generate_number(cls):
        import time
        return  "TR" + str(int(time.time()))

    @classmethod
    def search(cls, **attrs):
        bankcard_qs = cls.query().filter(**attrs)
        return bankcard_qs

    @classmethod
    def create(cls, **transacation_record):
        transacation_record.update({"number": cls.generate_number()})
        return super(CustomerTransactionRecord, cls).create(**transacation_record)


class CustomerTransactionInputRecord(BaseModel):
    """客户入账记录"""
    number = CharField(verbose_name = "入账交易编号", max_length = 48)
    amount = IntegerField(verbose_name = "金额，单位：分") # 有正负之分
    pay_type = CharField(verbose_name = "支付方式", max_length = 12, choices = PayTypes.CHOICES)
    status = CharField(verbose_name = "交易状态", max_length = 24, choices = TransactionStatus.CHOICES, default = TransactionStatus.PAY_FINISH)
    remark = TextField(verbose_name = "记录备注", default = "")

    business_type = CharField(verbose_name = "业务来源", max_length = 16, choices = BusinessTypes.CHOICES)
    business_id = IntegerField(verbose_name = "业务ID", null = True) # 需要确认来源凭证ID，进出账都可以：包含余额id，订单id，红包id等

    customer = ForeignKey(Customer, on_delete=CASCADE)
    transaction = ForeignKey(CustomerTransactionRecord, null = True, on_delete=CASCADE)

    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)

    class Meta:
        db_table = "customer_transaction_input_record"

    @classmethod
    def generate_number(cls):
        import time
        return  "TRI" + str(int(time.time()))

    @classmethod
    def create(cls, **input_infos):
        input_infos.update({"number": cls.generate_number()})
        input_record = super(CustomerTransactionInputRecord, cls).create(**input_infos)
        return input_record

    def update(self, **output_infos):
        self = super(CustomerTransactionInputRecord, self).update(**output_infos)
        if self.status == TransactionStatus.ACCOUNT_FINISH and self.transaction is None:
            transacation_record = CustomerTransactionRecord.create(
                amount =  self.amount,
                pay_type = self.pay_type,
                remark = self.remark,
                input_record_id = self.id,
                business_type = self.business_type,
                business_id = self.business_id,
                customer = self.customer,
                create_time = self.create_time,
            )
            self.update(transaction = transacation_record)
        return self


    @classmethod
    def search(cls, **attrs):
        bankcard_qs = cls.query().filter(**attrs)
        return bankcard_qs


class CustomerTransactionOutputRecord(BaseModel):
    """客户出账记录"""
    number = CharField(verbose_name = "出账交易编号", max_length = 48)
    amount = IntegerField(verbose_name = "金额，单位：分") # 有正负之分
    pay_type = CharField(verbose_name = "支付方式", max_length = 12, choices = PayTypes.CHOICES)
    status = CharField(verbose_name = "交易状态", max_length = 24, choices = TransactionStatus.CHOICES, default = TransactionStatus.PAY_FINISH)
    remark = TextField(verbose_name = "记录备注", default = "")

    business_type = CharField(verbose_name = "业务来源", max_length = 16, choices = BusinessTypes.CHOICES)
    business_id = IntegerField(verbose_name = "业务ID", null = True) # 需要确认来源凭证ID，进出账都可以：包含余额id，订单id，红包id等

    customer = ForeignKey(Customer, on_delete=CASCADE)
    transaction = ForeignKey(CustomerTransactionRecord, null = True, on_delete=CASCADE)

    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)

    class Meta:
        db_table = "customer_transaction_output_record"

    @classmethod
    def generate_number(cls):
        import time
        return  "TRO" + str(int(time.time()))

    @classmethod
    def search(cls, **attrs):
        bankcard_qs = cls.query().filter(**attrs)
        return bankcard_qs

    @classmethod
    def create(cls, **output_infos):
        output_infos.update({"number": cls.generate_number()})
        output_record = super(CustomerTransactionOutputRecord, cls).create(**output_infos)
        if output_record:
            transacation_record = CustomerTransactionRecord.create(
                amount = output_record.amount,
                pay_type = output_record.pay_type,
                remark = output_record.remark,
                output_record_id = output_record.id,
                business_type = output_record.business_type,
                business_id = output_record.business_id,
                customer = output_record.customer,
                create_time = output_record.create_time,
            )
            output_record.update(transaction = transacation_record)
        return output_record


class CustomerBalanceRecord(BaseModel):
    """客户余额记录"""
    number = CharField(verbose_name = "交易编号", max_length = 48)
    amount = IntegerField(verbose_name = "金额，单位：分") # 有正负之分
    pay_type = CharField(verbose_name = "支付方式", max_length = 12, choices = PayTypes.CHOICES)
    remark = TextField(verbose_name = "记录备注", default = "")

    input_record = ForeignKey(CustomerTransactionInputRecord, null = True, on_delete=CASCADE)
    output_record = ForeignKey(CustomerTransactionOutputRecord, null = True, on_delete=CASCADE)

    customer = ForeignKey(Customer, on_delete=CASCADE)

    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)

    class Meta:
        db_table = "customer_balance_record"

    @classmethod
    def generate_number(cls):
        import time
        return  "BL" + str(int(time.time()))

    @classmethod
    def get_balance(cls, customer):
        result = CustomerTransactionRecord.search(
                    customer = customer,
                    business_type = BusinessTypes.BALANCE
                ).aggregate(total=Sum('amount'))
        if result['total'] is None:
            return 0
        return result['total']

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
