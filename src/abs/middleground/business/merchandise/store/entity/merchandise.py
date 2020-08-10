# coding=UTF-8
'''
Created on 2020年7月10日

@author: Administrator
'''

from abs.common.model import BaseModel, IntegerField, \
        CharField, DateTimeField, TextField, timezone
from abs.middleground.business.merchandise.utils.constant import \
        DespatchService, UseStatus
from abs.middleground.business.merchandise.settings import DB_PREFIX


class Merchandise(BaseModel):
    """
    商品信息表
    """
    title = CharField(verbose_name="商品标题", max_length=256)
    description = CharField(verbose_name="商品描述", max_length=256)
    slideshow = TextField(verbose_name="商品轮播图")
    video_display = TextField(verbose_name="展示视频")
    detail = TextField(verbose_name="商品详情")
    market_price = IntegerField(verbose_name="市场价格，单位：分")

    pay_types = CharField(
        verbose_name="支付方式",
        max_length=128
    )
    pay_services = CharField(
        verbose_name="支付服务",
        max_length=128
    )
    despatch_type = CharField(
        verbose_name="发货方式",
        choices=DespatchService.CHOICES,
        max_length=64
    )

    use_status = CharField(
        verbose_name="使用状态",
        choices=UseStatus.CHOICES,
        default=UseStatus.FORBIDDENT,
        max_length=64
    )
    company_id = IntegerField(verbose_name="公司ID")
    production_id = IntegerField(verbose_name="产品ID")
    remark = TextField(verbose_name="备注")
    update_time = DateTimeField(verbose_name="更新时间", auto_now=True)
    create_time = DateTimeField(verbose_name="创建时间", default=timezone.now)

    class Meta:
        db_table = DB_PREFIX + "base"
        unique_together = (
            ('company_id', 'title'),
        )

    @classmethod
    def get_bytitle(cls, company_id, title):
        merchandise_qs = cls.search(
            company_id=company_id,
            title=title
        )
        if merchandise_qs.count():
            return merchandise_qs[0]
        return None

    @classmethod
    def search(cls, **attrs):
        merchandise_qs = cls.query().filter(**attrs)
        return merchandise_qs
