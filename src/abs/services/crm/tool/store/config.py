# coding=UTF-8

from abs.common.model import BaseModel, BooleanField, \
        IntegerField, CharField, TextField, DateTimeField, timezone
from abs.services.crm.tool.settings import DB_PREFIX


class Config(BaseModel):
    type_desc = CharField(verbose_name = "类别描述", max_length = 64)
    type = CharField(verbose_name = "类别", max_length = 64)
    name = CharField(verbose_name = "名称", max_length = 64)
    key = CharField(verbose_name = "key", max_length = 64)
    value = TextField(verbose_name = "value", default = "")

    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)


    class Meta:
        db_table = DB_PREFIX + "config"

    @classmethod
    def search(cls, **attrs):
        config_qs = cls.query().filter(**attrs)
        return config_qs
