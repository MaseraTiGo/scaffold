# coding=UTF-8

from abs.common.model import BaseModel, BooleanField, ForeignKey, \
        IntegerField, CharField, TextField, DateTimeField, timezone, CASCADE
from abs.services.agent.goods.settings import DB_PREFIX
from abs.services.agent.goods.utils.constant import ReviewStatus


class Goods(BaseModel):
    school_id = IntegerField(verbose_name = "学校id")
    major_id = IntegerField(verbose_name = "专业id")
    agent_id = IntegerField(verbose_name = "代理商id", null = True)
    relations_id = IntegerField(verbose_name = '学校专业id', default = 0)
    years_id = IntegerField(verbose_name = "学年id", default = 0)
    template_id = IntegerField(verbose_name = "合同模板id", default = 0)
    merchandise_id = IntegerField(verbose_name = '通用商品id', default = 0)
    is_hot = BooleanField(verbose_name = "是否热门", default = False)

    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)

    class Meta:
        db_table = DB_PREFIX + "base"

    @classmethod
    def search(cls, **attrs):
        goods_qs = cls.query().filter(**attrs)
        return goods_qs


class GoodsReview(BaseModel):
    goods = ForeignKey(Goods, on_delete=CASCADE)
    staff_id = IntegerField(verbose_name="审核人id", default=0)
    status = CharField(verbose_name="审核状态", max_length=64,
                       default=ReviewStatus.WAIT_POST,
                       choices=ReviewStatus.CHOICES)
    remark = TextField(verbose_name="审核备注", default='')
    update_time = DateTimeField(verbose_name="更新时间", auto_now=True)
    create_time = DateTimeField(verbose_name="创建时间", default=timezone.now)

    class Meta:
        db_table = DB_PREFIX + "review"

    @classmethod
    def search(cls, **attrs):
        goods_review_qs = cls.query().filter(**attrs)
        return goods_review_qs
