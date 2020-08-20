# coding=UTF-8

from abs.common.model import BaseModel, DateField, ForeignKey, \
        IntegerField, CharField, TextField, DateTimeField, timezone
from abs.services.agent.goods.settings import DB_PREFIX
from abs.services.agent.goods.store.goods import Goods


class Poster(BaseModel):
    goods = ForeignKey(Goods)
    phone = CharField(verbose_name="手机号", max_length=16, default='')
    expire_date = DateField(verbose_name="过期天数")
    remark = TextField(verbose_name="说明")

    update_time = DateTimeField(verbose_name="更新时间", auto_now=True)
    create_time = DateTimeField(verbose_name="创建时间", default=timezone.now)

    class Meta:
        db_table = DB_PREFIX + "poster"

    @classmethod
    def search(cls, **attrs):
        poster_qs = cls.query().filter(**attrs)
        return poster_qs


class PosterSpecification(BaseModel):
    poster = ForeignKey(Poster)
    specification_id = IntegerField(verbose_name="规格id")
    sale_price = IntegerField(verbose_name="价格")

    update_time = DateTimeField(verbose_name="更新时间", auto_now=True)
    create_time = DateTimeField(verbose_name="创建时间", default=timezone.now)

    class Meta:
        db_table = DB_PREFIX + "poster_specification"

    @classmethod
    def search(cls, **attrs):
        poster_qs = cls.query().filter(**attrs)
        return poster_qs
