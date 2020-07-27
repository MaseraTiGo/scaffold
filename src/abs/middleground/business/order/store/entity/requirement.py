# coding=UTF-8

'''
Created on 2020年7月10日

@author: Roy
'''

from abs.common.model import BaseModel, CASCADE, TextField,\
        IntegerField, CharField, DateTimeField, ForeignKey, timezone
from abs.middleground.business.order.settings import DB_PREFIX


class Requirement(BaseModel):
    """
    需求单
    """
    sale_price = IntegerField(verbose_name="销售价位，单位：分")

    update_time = DateTimeField(verbose_name="更新时间", auto_now=True)
    create_time = DateTimeField(verbose_name="创建时间", default=timezone.now)

    class Meta:
        db_table = DB_PREFIX + "requirement"


class MerchandiseSnapShoot(BaseModel):
    """
    商品快照
    """
    production_id = IntegerField(verbose_name="产品ID")
    merchandise_id = IntegerField(verbose_name="商品ID")
    specification_id = IntegerField(verbose_name="商品g规格ID")

    title = CharField(verbose_name="商品标题", max_length=256)
    show_image = CharField(verbose_name="展示图片", max_length=256)
    remark = TextField(verbose_name="快照备注")

    sale_price = IntegerField(verbose_name="销售单价，单位：分")
    count = IntegerField(verbose_name="商品购买数量")
    total_price = IntegerField(verbose_name="总价，单位：分")

    requirement = ForeignKey(Requirement, on_delete=CASCADE)
    update_time = DateTimeField(verbose_name="更新时间", auto_now=True)
    create_time = DateTimeField(verbose_name="创建时间", default=timezone.now)

    class Meta:
        db_table = DB_PREFIX + "snapshoot"
