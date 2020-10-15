# coding=UTF-8

from abs.common.model import BaseModel, IntegerField, CharField, DateTimeField, timezone, \
        ForeignKey, CASCADE, TextField
from abs.services.crm.university.utils.constant import DurationTypes, CategoryTypes

from abs.services.agent.order.settings import DB_PREFIX
from abs.services.agent.order.store.order import Order
from abs.services.agent.order.utils.constant import EvaluationTypes


class OrderItem(BaseModel):
    order = ForeignKey(Order, on_delete = CASCADE)
    goods_id = IntegerField(verbose_name = "商品id")
    merchandise_snapshoot_id = IntegerField(verbose_name = "商品快照id")
    template_id = IntegerField(verbose_name = "合同模板id", default = 0)
    school_name = CharField(verbose_name = "学校名称", max_length = 32, default = "")
    school_city = CharField(verbose_name = "学校城市", max_length = 32, default = '')
    major_name = CharField(verbose_name = "专业名称", max_length = 64, default = "")
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

    evaluation = CharField(
        verbose_name="评价状态",
        max_length=32,
        choices = EvaluationTypes.CHOICES,
        default = EvaluationTypes.WAIT_EVALUATION
    )

    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)

    class Meta:
        db_table = DB_PREFIX + "orderitem"

    @classmethod
    def search(cls, **attrs):
        orderitem_qs = cls.query().filter(**attrs)
        return orderitem_qs


class OrderItemEvaluation(BaseModel):
    order_item = ForeignKey(OrderItem, verbose_name="订单物品id")

    person_id = IntegerField(verbose_name = "用户id")
    goods_id = IntegerField(verbose_name = "商品id")
    tags = TextField(verbose_name="评价标签", default='[]')
    content = TextField(verbose_name="评价内容", default='')
    pics = TextField(verbose_name='评价图片', default='[]')
    videos = TextField(verbose_name="评价视频", default='[]')
    server_attitude = IntegerField(verbose_name="服务态度", default=0)
    course_quality = IntegerField(verbose_name="课程质量", default=0)
    major = IntegerField(verbose_name="院校专业", default=0)
    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)

    class Meta:
        db_table = DB_PREFIX + "evaluation"

    @classmethod
    def search(cls, **attrs):
        evaluation_qs = cls.query().filter(**attrs)
        return evaluation_qs