# coding=UTF-8

'''
Created on 2020年7月10日

@author: Administrator
'''

from abs.common.model import BaseModel, \
        CharField, DateTimeField, TextField, timezone
from abs.middleground.support.logistics.settings import DB_PREFIX
from abs.middleground.support.logistics.utils.constant import \
        LogisticsCompany, LogisticsStatus


class Logistics(BaseModel):
    """
    物流信息表
    """
    sender_name = CharField(verbose_name="发送人", max_length=32)
    sender_phone = CharField(verbose_name="发送人电话", max_length=32)
    sender_address = CharField(verbose_name="发送地址", max_length=32)

    receiver_name = CharField(verbose_name="收件人", max_length=32)
    receiver_phone = CharField(verbose_name="收件人电话", max_length=32)
    receiver_address = CharField(verbose_name="收件人地址", max_length=32)

    status = CharField(
        verbose_name="物流状态",
        max_length=32,
        choices=LogisticsStatus.CHOICES,
        default=LogisticsStatus.PERPARE,
    )
    transit_company = CharField(
        verbose_name="物流公司",
        max_length=24,
        choices=LogisticsCompany.CHOICES,
    )
    transit_number = CharField(
        verbose_name="物流订单号",
        max_length=128,
        default=""
    )

    remark = TextField(verbose_name="备注")
    update_time = DateTimeField(verbose_name="更新时间", auto_now=True)
    create_time = DateTimeField(verbose_name="创建时间", default=timezone.now)

    class Meta:
        db_table = DB_PREFIX + "base"
        unique_together = (
            ("transit_company", 'transit_number'),
        )
