# coding=UTF-8

from abs.common.model import BaseModel, DateField, ForeignKey, \
        IntegerField, CharField, TextField, DateTimeField, timezone, \
        CASCADE
from abs.services.agent.goods.settings import DB_PREFIX
from abs.services.agent.goods.store.goods import Goods
from abs.middleground.business.transaction.utils.constant import PayService

class Poster(BaseModel):
    goods = ForeignKey(Goods, on_delete = CASCADE)
    staff_id = IntegerField(verbose_name = "员工id", default = 0)
    phone = CharField(verbose_name = "手机号", max_length = 16, default = '')
    expire_date = DateField(verbose_name = "过期天数")
    remark = TextField(verbose_name = "说明")
    pay_services = CharField(
        verbose_name = "订单支付服务",
        max_length = 128,
        choices = PayService.CHOICES,
        default = PayService.FULL_PAYMENT
    )
    pay_plan = TextField(verbose_name = "剩余款项汇款计划", default = "[]")
    deposit = IntegerField(verbose_name = "首付款", default = 0)
    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)

    class Meta:
        db_table = DB_PREFIX + "poster"

    @classmethod
    def search(cls, **attrs):
        poster_qs = cls.query().filter(**attrs)
        return poster_qs


class PosterSpecification(BaseModel):
    poster = ForeignKey(Poster, on_delete = CASCADE)
    specification_id = IntegerField(verbose_name = "规格id")
    sale_price = IntegerField(verbose_name = "价格")

    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)

    class Meta:
        db_table = DB_PREFIX + "poster_specification"

    @classmethod
    def search(cls, **attrs):
        poster_qs = cls.query().filter(**attrs)
        return poster_qs
