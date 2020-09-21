# coding=UTF-8

from abs.common.model import BaseModel, \
        IntegerField, CharField, TextField, DateTimeField, timezone


class AbstractCompany(BaseModel):
    name = CharField(verbose_name="公司名称", max_length=32)
    license_number = CharField(verbose_name="营业执照编号", max_length=32)
    permission_key = CharField(
        verbose_name="权限appkey",
        max_length=256,
        default=""
    )
    company_id = IntegerField(verbose_name="企业id")

    remark = TextField(verbose_name="备注")
    update_time = DateTimeField(verbose_name="更新时间", auto_now=True)
    create_time = DateTimeField(verbose_name="创建时间", default=timezone.now)

    class Meta:
        abstract = True

    @classmethod
    def is_exsited(cls, license_number):
        enterprise_qs = cls.search(license_number=license_number)
        if enterprise_qs.count() > 0:
            return True, enterprise_qs[0]
        return False, None
