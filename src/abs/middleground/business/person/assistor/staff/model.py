# coding=UTF-8

from abs.common.model import BaseModel, BooleanField,\
        IntegerField, CharField, TextField, DateTimeField, timezone


class AbstractStaff(BaseModel):

    work_number = CharField(verbose_name="工号", max_length=24)
    is_admin = BooleanField(verbose_name="是否是管理员", default=False)

    person_id = IntegerField(verbose_name="用户id")
    company_id = IntegerField(verbose_name="企业id")

    remark = TextField(verbose_name="备注")
    update_time = DateTimeField(verbose_name="更新时间", auto_now=True)
    create_time = DateTimeField(verbose_name="创建时间", default=timezone.now)

    class Meta:
        abstract = True
