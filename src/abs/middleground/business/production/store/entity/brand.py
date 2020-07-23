# coding=UTF-8

'''
Created on 2020年7月10日

@author: Administrator
'''

from abs.common.model import BaseModel, \
        IntegerField, CharField, DateTimeField, timezone
from abs.middleground.business.production.settings import DB_PREFIX
from abs.middleground.business.production.utils.constant import IndustryTypes


class Brand(BaseModel):
    """
    产品品牌
    """
    name = CharField(verbose_name="品牌名称", max_length=24)
    industry = CharField(
        verbose_name="行业",
        choices=IndustryTypes.CHOICES,
        max_length=24
    )
    description = CharField(verbose_name="品牌描述", max_length=256)

    company_id = IntegerField(verbose_name="公司ID")
    update_time = DateTimeField(verbose_name="更新时间", auto_now=True)
    create_time = DateTimeField(verbose_name="创建时间", default=timezone.now)

    class Meta:
        db_table = DB_PREFIX + "brand"
