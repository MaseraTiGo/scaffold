# coding=UTF-8

from abs.common.model import BaseModel, BooleanField, \
        IntegerField, CharField, TextField, DateTimeField, timezone, \
        ForeignKey, CASCADE
from abs.services.crm.university.settings import DB_PREFIX
from abs.services.crm.university.store import Relations
from abs.services.crm.university.utils.constant import DurationTypes, \
     CategoryTypes


class Years(BaseModel):
    relations = ForeignKey(Relations, on_delete = CASCADE)
    category = CharField(
        verbose_name = "类别",
        max_length = 64,
        choices = CategoryTypes.CHOICES,
        default = CategoryTypes.OTHER
    )
    duration = CharField(
        verbose_name = "时长",
        max_length = 32,
        choices = DurationTypes.CHOICES,
        default = DurationTypes.OTHER
    )

    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)

    class Meta:
        db_table = DB_PREFIX + "years"

    @classmethod
    def search(cls, **attrs):
        years_qs = cls.query().filter(**attrs)
        return years_qs
