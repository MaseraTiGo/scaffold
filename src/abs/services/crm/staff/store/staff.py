# coding=UTF-8

from abs.common.model import BaseModel, BooleanField,\
        IntegerField, CharField, TextField, DateTimeField, timezone
from abs.services.crm.staff.settings import DB_PREFIX


class Staff(BaseModel):

    nick = CharField(verbose_name="昵称", max_length=32)
    head_url = CharField(verbose_name="头像URL", max_length=256, default="")

    work_number = CharField(verbose_name="工号", max_length=24)
    is_admin = BooleanField(verbose_name="是否是管理员", default=False)

    person_id = IntegerField(verbose_name="用户id")
    company_id = IntegerField(verbose_name="企业id")

    remark = TextField(verbose_name="备注")
    update_time = DateTimeField(verbose_name="更新时间", auto_now=True)
    create_time = DateTimeField(verbose_name="创建时间", default=timezone.now)

    class Meta:
        db_table = DB_PREFIX + "base"

    @classmethod
    def search(cls, **attrs):
        staff_qs = cls.query().filter(**attrs)
        return staff_qs
