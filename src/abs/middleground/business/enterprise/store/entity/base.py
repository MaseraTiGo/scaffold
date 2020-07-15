# coding=UTF-8

'''
Created on 2020年7月10日

@author: Administrator
'''

from abs.common.model import BaseModel, \
        CharField, DateTimeField, timezone
from abs.middleground.business.enterprise.settings import DB_PREFIX


class Enterprise(BaseModel):
    """
    公司信息表
    """
    name = CharField(verbose_name="公司名称", max_length=32)
    license_number = CharField(verbose_name="营业执照编号", max_length=32)
    license_url = CharField(verbose_name="营业执照", max_length=256, default="")

    update_time = DateTimeField(verbose_name="更新时间", auto_now=True)
    create_time = DateTimeField(verbose_name="创建时间", default=timezone.now)

    class Meta:
        db_table = DB_PREFIX + "base"
        unique_together = ("license_number",)

    @classmethod
    def search(cls, **attrs):
        enterprise_qs = cls.query().filter(**attrs)
        return enterprise_qs

    @classmethod
    def is_exsited(cls, license_number):
        enterprise_qs = cls.search(license_number=license_number)
        if enterprise_qs.count() > 0:
            return True, enterprise_qs[0]
        return False, None
