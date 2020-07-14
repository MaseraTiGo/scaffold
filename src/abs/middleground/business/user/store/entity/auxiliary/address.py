# coding=UTF-8

from abs.common.model import CASCADE,\
        BaseModel, ForeignKey, CharField, DateTimeField, timezone
from abs.middleground.business.user.settings import DB_PREFIX
from abs.middleground.business.user.store.entity.base import User
from abs.middleground.business.user.utils.constant import GenderTypes


class Address(BaseModel):

    contacts = CharField(verbose_name="联系人", max_length=64)
    gender = CharField(
        verbose_name="性别",
        max_length=24,
        choices=GenderTypes.CHOICES,
        default=GenderTypes.UNKNOWN
    )
    phone = CharField(verbose_name="联系电话", max_length=64)

    city = CharField(verbose_name="城市", max_length=64)
    address = CharField(verbose_name="详细地址", max_length=256)

    user = ForeignKey(User, on_delete=CASCADE)

    update_time = DateTimeField(verbose_name="更新时间", auto_now=True)
    create_time = DateTimeField(verbose_name="创建时间", default=timezone.now)

    class Meta:
        db_table = DB_PREFIX + "adddress"

    @classmethod
    def search(cls, **attrs):
        address_qs = cls.query().filter(**attrs)
        return address_qs
