# coding=UTF-8


import uuid
import time

from abs.common.model import BaseModel, IntegerField,\
        CharField, DateTimeField, TextField, ForeignKey, CASCADE, timezone
from abs.middleground.technology.permission.settings import DB_PREFIX
from abs.middleground.technology.permission.utils.constant import \
        UseStatus, PermissionTypes


class PlatForm(BaseModel):
    """
    平台
    """
    name = CharField(verbose_name="平台名称", max_length=64)
    company_id = IntegerField(verbose_name="公司Id(平台归属哪家公司)")
    company_name = CharField(verbose_name="公司名称(平台归属哪家公司)", max_length=256)
    app_type = CharField(
        verbose_name="授权类型",
        max_length=24,
        choices=PermissionTypes.CHOICES
    )
    remark = TextField(verbose_name="备注")
    update_time = DateTimeField(verbose_name="更新时间", auto_now=True)
    create_time = DateTimeField(verbose_name="创建时间", default=timezone.now)

    class Meta:
        db_table = DB_PREFIX + "platform"
        unique_together = (
            ('name',)
        )


class Authorization(BaseModel):
    """
    授权
    """
    appkey = CharField(verbose_name="授权appkey", max_length=48)
    use_status = CharField(
        verbose_name="使用状态",
        max_length=24,
        choices=UseStatus.CHOICES,
        default=UseStatus.FORBIDDEN,
    )
    company_id = IntegerField(verbose_name="使用权限的公司")
    company_name = CharField(verbose_name="公司名称", max_length=256)
    platform = ForeignKey(PlatForm, on_delete=CASCADE)
    remark = TextField(verbose_name="备注")
    update_time = DateTimeField(verbose_name="更新时间", auto_now=True)
    create_time = DateTimeField(verbose_name="创建时间", default=timezone.now)

    class Meta:
        db_table = DB_PREFIX + "platform_company"
        unique_together = (
            ('company_id', 'platform')
        )

    @classmethod
    def generate_appkey(cls):
        return uuid.uuid3(uuid.NAMESPACE_DNS, str(time.time()))

    @classmethod
    def create(cls, **authorization_info):
        authorization_info.update({
            'appkey': cls.generate_appkey()
        })
        return super(Authorization, cls).create(
            **authorization_info
        )

    @classmethod
    def get_byappkey(cls, appkey):
        authorization_qs = cls.query(
            appkey=appkey
        )
        if authorization_qs.count() > 0:
            return authorization_qs[0]
        return None

    @classmethod
    def get_byplatform(cls, platform):
        authorization_qs = cls.query(
            platform=platform
        )
        return list(authorization_qs)

    @classmethod
    def check_unique(cls, platform_id, company_id):
        authorization_qs = cls.search(
            platform_id=platform_id,
            company_id=company_id,
        )
        return authorization_qs.count() > 0
