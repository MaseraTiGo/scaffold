# coding=UTF-8

from abs.common.model import BaseModel, CharField, DateTimeField, timezone, TextField
from abs.services.crm.tool.settings import DB_PREFIX
from abs.services.crm.tool.utils.contact import NoticeStatus, NoticePlatform, NoticeClassify


class Notice(BaseModel):
    title = CharField(verbose_name="标题", max_length=64, default='')
    content = TextField(verbose_name="内容", max_length=64, default='')

    classify = CharField(
        verbose_name="类别：通知/公告",
        max_length=32,
        choices=NoticeClassify.CHOICES,
        default=NoticeClassify.NOTIFY
    )

    platform = CharField(
        verbose_name="通知（公告）来源平台",
        max_length=64,
        choices=NoticePlatform.CHOICES,
        default=NoticePlatform.CRM

    )

    status = CharField(
        verbose_name="通知（公告）状态",
        max_length=32,
        choices=NoticeStatus.CHOICES,
        default=NoticeStatus.ENABLE

    )

    update_time = DateTimeField(verbose_name="更新时间", auto_now=True)
    create_time = DateTimeField(verbose_name="创建时间", default=timezone.now)

    class Meta:
        db_table = DB_PREFIX + "notice"

    @classmethod
    def search(cls, **attrs):
        notice_qs = cls.query().filter(**attrs)
        return notice_qs
