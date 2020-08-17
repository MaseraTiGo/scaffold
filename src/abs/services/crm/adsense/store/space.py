# coding=UTF-8

from abs.common.model import BaseModel, BooleanField,\
        IntegerField, CharField, TextField, DateTimeField, timezone
from abs.services.crm.adsense.settings import DB_PREFIX


class Space(BaseModel):
    label = CharField(verbose_name="标签", max_length=128)
    name = CharField(verbose_name="广告位名称", max_length=256)
    width = IntegerField(verbose_name="宽度")
    height = IntegerField(verbose_name="高度")
    is_enable = BooleanField(verbose_name="是否使用", default=False)

    update_time = DateTimeField(verbose_name="更新时间", auto_now=True)
    create_time = DateTimeField(verbose_name="创建时间", default=timezone.now)

    class Meta:
        db_table = DB_PREFIX + "space"

    @classmethod
    def search(cls, **attrs):
        space_qs = cls.query().filter(**attrs)
        return space_qs
