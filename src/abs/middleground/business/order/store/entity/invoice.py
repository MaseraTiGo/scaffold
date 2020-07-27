# coding=UTF-8

'''
Created on 2020年7月10日

@author: Roy
'''

from abs.common.model import BaseModel, CASCADE,\
        IntegerField, CharField, DateTimeField, TextField,\
        ForeignKey, timezone
from abs.middleground.business.production.settings import DB_PREFIX
from abs.middleground.business.merchandise.utils.constant import \
        DespatchService
from abs.middleground.support.logistics.models import \
        Logistics
from abs.middleground.business.order.store.entity.requirement import \
        Requirement, MerchandiseSnapShoot


class Invoice(BaseModel):
    """
    发货单

    基于不同的发货类型，展现不同的字段，如：
        物流方式：name，phone，address
        手机充值：phne
        教育交付：name，phone，identification
    """
    name = CharField(verbose_name="姓名", max_length=16, default="")
    phone = CharField(verbose_name="手机号", max_length=24, default="")
    address = CharField(verbose_name="地址", max_length=256, default="")
    identification = CharField(verbose_name="身份证号", max_length=24, default="")

    requirement = ForeignKey(Requirement, on_delete=CASCADE)
    update_time = DateTimeField(verbose_name="更新时间", auto_now=True)
    create_time = DateTimeField(verbose_name="创建时间", default=timezone.now)

    class Meta:
        db_table = DB_PREFIX + "invoice"


class DeliveryRecord(BaseModel):
    """
    发货记录
    此处基于不同的发货类型，进行不同的交付外链
        物流方式 --> 物流信息表
        手机充值 --> 手机充值表
        教育交付 --> 教育合同表
    """
    despatch_type = CharField(
        verbose_name="发货方式",
        choices=DespatchService.CHOICES,
        max_length=64
    )
    despatch_id = IntegerField(verbose_name="发送ID")
    remark = TextField(verbose_name="记录备注", default="")

    invoice = ForeignKey(Invoice, on_delete=CASCADE)
    update_time = DateTimeField(verbose_name="更新时间", auto_now=True)
    create_time = DateTimeField(verbose_name="创建时间", default=timezone.now)

    class Meta:
        db_table = DB_PREFIX + "delivery_record"


class DeliveryRecordList(BaseModel):
    """
    发货记录明细
    """
    delivery_count = IntegerField(verbose_name="发货数量")
    snapshoot = ForeignKey(MerchandiseSnapShoot, on_delete=CASCADE)
    delivery_record = ForeignKey(DeliveryRecord, on_delete=CASCADE)
    create_time = DateTimeField(verbose_name="创建时间", default=timezone.now)

    class Meta:
        db_table = DB_PREFIX + "delivery_record_list"
