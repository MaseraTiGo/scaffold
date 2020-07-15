# coding=UTF-8

from abs.common.model import CASCADE,\
        BaseModel, ForeignKey, CharField, DateTimeField, timezone
from abs.middleground.business.person.settings import DB_PREFIX
from abs.middleground.business.person.store.entity.base import Person


class BankCard(BaseModel):

    bank_name = CharField(verbose_name="银行名称", max_length=24)
    bank_code = CharField(verbose_name="银行编码", max_length=20)
    bank_number = CharField(verbose_name="银行卡号", max_length=64)
    name = CharField(verbose_name="开户人姓名", max_length=16)
    phone = CharField(verbose_name="开户人手机号", max_length=20)
    identification = CharField(verbose_name="开户人身份证", max_length=24)

    person = ForeignKey(Person, on_delete=CASCADE)

    update_time = DateTimeField(verbose_name="更新时间", auto_now=True)
    create_time = DateTimeField(verbose_name="创建时间", default=timezone.now)

    class Meta:
        db_table = DB_PREFIX + "bankcard"

    @classmethod
    def search(cls, **attrs):
        bankcard_qs = cls.query().filter(**attrs)
        return bankcard_qs
