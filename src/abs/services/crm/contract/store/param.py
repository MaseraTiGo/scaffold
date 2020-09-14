# coding=UTF-8

from abs.common.model import BaseModel, BooleanField, \
        IntegerField, CharField, TextField, DateTimeField, timezone
from abs.services.crm.contract.settings import DB_PREFIX
from abs.services.crm.contract.utils.constant import ValueSource, KeyType


class Param(BaseModel):
    name = CharField(verbose_name = "参数名称", max_length = 64)
    name_key = CharField(verbose_name = "参数key值", max_length = 64)
    key_type = CharField(
        verbose_name = "参数类型",
        max_length = 64,
        choices = KeyType.CHOICES,
        default = KeyType.OTHER
    )
    default_value = CharField(verbose_name = "默认值", max_length = 256)
    actual_value_source = CharField(
        verbose_name = "实际值来源对象",
        max_length = 64,
        choices = ValueSource.CHOICES,
        default = ValueSource.COMPANY
    )

    is_allowed = BooleanField(verbose_name = "是否允许修改", default = True)

    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)


    class Meta:
        db_table = DB_PREFIX + "param"

    @classmethod
    def search(cls, **attrs):
        param_qs = cls.query().filter(**attrs)
        return param_qs
