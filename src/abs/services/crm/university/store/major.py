# coding=UTF-8

from abs.common.model import BaseModel, BooleanField, \
        IntegerField, CharField, TextField, DateTimeField, timezone
from abs.services.crm.tool.settings import DB_PREFIX
from abs.services.crm.tool.utils.contact import StatusTypes, SourceTypes, SceneTypes


class Major(BaseModel):
    name = CharField(verbose_name="专业名称", max_length=32)
    content = TextField(verbose_name="专业描述")
    sort = IntegerField(verbose_name="排序", default=0)
    is_hot = BooleanField(verbose_name="是否热门", default=False)

    update_time = DateTimeField(verbose_name="更新时间", auto_now=True)
    create_time = DateTimeField(verbose_name="创建时间", default=timezone.now)

    class Meta:
        db_table = DB_PREFIX + "major"

    @classmethod
    def search(cls, **attrs):
        major_qs = cls.query().filter(**attrs)
        return major_qs
