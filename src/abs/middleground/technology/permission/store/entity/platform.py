# coding=UTF-8


import uuid
import time

from abs.common.model import BaseModel, IntegerField,\
        CharField, DateTimeField, TextField, timezone
from abs.middleground.technology.permission.settings import DB_PREFIX
from abs.middleground.technology.permission.utils.constant import \
        PermissionTypes, UseStatus


class PlatForm(BaseModel):
    """
    授权平台
    """
    name = CharField(verbose_name="平台名称", max_length=64)
    company_id = IntegerField(verbose_name="公司id")
    appkey = CharField(verbose_name="授权appkey", max_length=48)
    app_type = CharField(
        verbose_name="授权类型",
        max_length=24,
        choices=PermissionTypes.CHOICES
    )
    use_status = CharField(
        verbose_name="使用状态",
        max_length=24,
        choices=UseStatus.CHOICES,
        default=UseStatus.FORBIDDEN,
    )
    prefix = CharField(verbose_name="公司前缀", max_length=8)
    remark = TextField(verbose_name="备注")
    update_time = DateTimeField(verbose_name="更新时间", auto_now=True)
    create_time = DateTimeField(verbose_name="创建时间", default=timezone.now)

    class Meta:
        db_table = DB_PREFIX + "platform"
        unique_together = (
            ('name',)
        )

    @classmethod
    def generate_appkey(cls):
        return uuid.uuid3(uuid.NAMESPACE_DNS, str(time.time()))

    @classmethod
    def create(cls, **platform_info):
        platform_info.update({
            'appkey': cls.generate_appkey()
        })
        return super(PlatForm, cls).create(
            **platform_info
        )

    @classmethod
    def get_byappkey(cls, appkey):
        platform_qs = cls.query(
            appkey=appkey
        )
        if platform_qs.count() > 0:
            return platform_qs[0]
        return None
