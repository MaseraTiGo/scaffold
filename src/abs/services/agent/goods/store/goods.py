# coding=UTF-8

from abs.common.model import BaseModel, BooleanField, ForeignKey, \
        IntegerField, CharField, TextField, DateTimeField, timezone
from abs.services.agent.goods.settings import DB_PREFIX
from abs.services.agent.goods.utils.constant import DurationTypes, \
     CategoryTypes


class Goods(BaseModel):
    school_id = IntegerField(verbose_name = "学校id")
    major_id = IntegerField(verbose_name = "专业id")
    agent_id = IntegerField(verbose_name = "代理商id", null = True)
    merchandise_id = IntegerField(verbose_name = '通用商品id')
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
    is_hot = BooleanField(verbose_name = "是否热门", default = False)

    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)

    class Meta:
        db_table = DB_PREFIX + "base"

    @classmethod
    def search(cls, **attrs):
        goods_qs = cls.query().filter(**attrs)
        return goods_qs
