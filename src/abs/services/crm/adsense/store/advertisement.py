# coding=UTF-8

from abs.common.model import BaseModel, BooleanField, ForeignKey,\
        IntegerField, CharField, TextField, DateTimeField, timezone
from abs.services.crm.adsense.settings import DB_PREFIX
from .space import Space


class Advertisement(BaseModel):
    space = ForeignKey(Space)
    thumbnail = TextField(verbose_name="缩略图")
    name = CharField(verbose_name="广告名称", max_length=256)
    url = TextField(verbose_name="跳转地址", default='')
    sort = IntegerField(verbose_name="排序", default=0)

    update_time = DateTimeField(verbose_name="更新时间", auto_now=True)
    create_time = DateTimeField(verbose_name="创建时间", default=timezone.now)

    class Meta:
        db_table = DB_PREFIX + "advertisement"

    @classmethod
    def search(cls, **attrs):
        ad_qs = cls.query().filter(**attrs)
        return ad_qs
