# coding=UTF-8

from abs.common.model import BaseModel, BooleanField, TextField, \
        IntegerField, CharField, DateTimeField, timezone, \
        ForeignKey, CASCADE
from abs.services.customer.personal.settings import DB_PREFIX
from abs.services.customer.personal.store import Customer
from abs.services.customer.personal.utils.constant import FeedType, FeedStatus


class Feedback(BaseModel):
    customer = ForeignKey(Customer, on_delete = CASCADE)
    type = CharField(
        verbose_name = "意见反馈类型",
        max_length = 128,
        choices = FeedType.CHOICES,
        default = FeedType.OTHER
    )
    status = CharField(
        verbose_name = "状态",
        max_length = 128,
        choices = FeedStatus.CHOICES,
        default = FeedStatus.WAIT_SOLVE
    )
    img_url = TextField(verbose_name = "图片", default = "[]")
    describe = TextField(verbose_name = "描述")
    remark = TextField(verbose_name = "备注")

    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)

    class Meta:
        db_table = DB_PREFIX + "feedback"

    @classmethod
    def search(cls, **attrs):
        feedback_qs = cls.query().filter(**attrs)
        return feedback_qs
