# coding=UTF-8

from abs.common.model import CASCADE,\
        BaseModel, ForeignKey, CharField, DateTimeField, timezone
from abs.middleground.business.person.settings import DB_PREFIX
from abs.middleground.business.person.utils.constant import EducationTypes
from abs.middleground.business.person.store.entity.base import Person


class Education(BaseModel):

    education = CharField(
        verbose_name="学历",
        max_length=24,
        choices=EducationTypes.CHOICES,
        default=EducationTypes.OTHER
    )

    person = ForeignKey(Person, on_delete=CASCADE)

    update_time = DateTimeField(verbose_name="更新时间", auto_now=True)
    create_time = DateTimeField(verbose_name="创建时间", default=timezone.now)

    class Meta:
        db_table = DB_PREFIX + "education"

    @classmethod
    def search(cls, **attrs):
        bankcard_qs = cls.query().filter(**attrs)
        return bankcard_qs
