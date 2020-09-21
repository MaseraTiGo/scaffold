# coding=UTF-8

from abs.common.model import BaseModel, BooleanField, \
        IntegerField, CharField, DateTimeField, timezone, \
        ForeignKey, CASCADE
from abs.services.customer.personal.settings import DB_PREFIX
from abs.services.customer.personal.store import Customer


class CollectionRecord(BaseModel):
    customer = ForeignKey(Customer, on_delete = CASCADE)
    goods_id = IntegerField(verbose_name = "用户id", default = 0)
    is_delete = BooleanField(verbose_name = "是否删除", default = False)


    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)

    class Meta:
        db_table = DB_PREFIX + "collection_record"

    @classmethod
    def search(cls, **attrs):
        collection_record_qs = cls.query().filter(**attrs)
        return collection_record_qs
