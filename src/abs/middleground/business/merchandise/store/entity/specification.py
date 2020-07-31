# coding=UTF-8
'''
Created on 2020年7月10日

@author: Administrator
'''

from abs.common.model import BaseModel, IntegerField, CASCADE,\
        CharField, DateTimeField, TextField, ForeignKey, timezone
from abs.middleground.business.merchandise.settings import DB_PREFIX
from abs.middleground.business.merchandise.store.entity.merchandise import \
        Merchandise


class Specification(BaseModel):
    """
    商品规格表
    """
    show_image = CharField(verbose_name="展示图片", max_length=256)
    sale_price = IntegerField(verbose_name="销售价格，单位：分")
    stock = IntegerField(verbose_name="库存")
    remark = TextField(verbose_name="备注")

    merchandise = ForeignKey(Merchandise, on_delete=CASCADE)
    update_time = DateTimeField(verbose_name="更新时间", auto_now=True)
    create_time = DateTimeField(verbose_name="创建时间", default=timezone.now)

    class Meta:
        db_table = DB_PREFIX + "specification"


class SpecificationValue(BaseModel):
    """
    商品规格值
    """
    category = CharField(verbose_name="属性分类", max_length=24)
    attribute = CharField(verbose_name="属性值", max_length=64)

    specification = ForeignKey(Specification, on_delete=CASCADE)
    update_time = DateTimeField(verbose_name="更新时间", auto_now=True)
    create_time = DateTimeField(verbose_name="创建时间", default=timezone.now)

    class Meta:
        db_table = DB_PREFIX + "specification_value"
