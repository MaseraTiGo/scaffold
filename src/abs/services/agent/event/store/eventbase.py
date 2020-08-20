# coding=UTF-8

from abs.common.model import BaseModel, BooleanField, \
        IntegerField, CharField, TextField, DateTimeField, timezone


class EventBase(BaseModel):
    """事件基类表"""
    agent_staff_id = IntegerField(verbose_name = "代理商员工id")

    organization_id = IntegerField(verbose_name = "组织id")

    remark = TextField(verbose_name = "备注", null = True, default = "")

    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)

    class Meta:
        abstract = True

    @classmethod
    def search(cls, **attrs):
        event_qs = cls.query().filter(**attrs)
        return event_qs
