# coding=UTF-8

from abs.common.model import BaseModel, BooleanField,\
        IntegerField, CharField, TextField, DateTimeField, timezone
from abs.services.crm.tool.settings import DB_PREFIX
from abs.services.crm.tool.utils.contact import StatusTypes, SourceTypes, SceneTypes


class SmsRecord(BaseModel):
    phone = CharField(verbose_name="手机号", max_length=32)
    template_id = CharField(verbose_name="模板id", max_length=64)
    template_label = CharField(verbose_name="模板标签", max_length=64)
    param = TextField(verbose_name="参数")
    content = TextField(verbose_name="内容")
    label = CharField(verbose_name="短信平台标签", max_length=64)
    unique_no = CharField(verbose_name="唯一标识", max_length=128)
    scene = CharField(
        verbose_name="场景标识",
        max_length=64,
        choices=SceneTypes.CHOICES
    )
    source_type = CharField(
        verbose_name="接收短信的用户来源平台",
        max_length=64,
        choices=SourceTypes.CHOICES
    )
    status = CharField(
        verbose_name="发送状态",
        max_length=32,
        choices=StatusTypes.CHOICES
    )

    update_time = DateTimeField(verbose_name="更新时间", auto_now=True)
    create_time = DateTimeField(verbose_name="创建时间", default=timezone.now)

    class Meta:
        db_table = DB_PREFIX + "smsrecord"

    @classmethod
    def search(cls, **attrs):
        record_qs = cls.query().filter(**attrs)
        return record_qs
