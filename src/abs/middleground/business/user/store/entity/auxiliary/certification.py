# coding=UTF-8

from abs.common.model import CASCADE, BaseModel,\
        ForeignKey, CharField, TextField, DateTimeField, timezone
from abs.middleground.business.user.settings import DB_PREFIX
from abs.middleground.business.user.store.entity.base import User


class Certification(BaseModel):

    name = CharField(verbose_name="姓名", max_length=64)
    identification = CharField(verbose_name="身份证号", max_length=24)
    id_front = CharField(verbose_name="身份证正面", max_length=256, default="")
    id_back = CharField(verbose_name="身份证反面", max_length=256, default="")
    id_in_hand = CharField(verbose_name="身份证反面", max_length=256, default="")
    remark = TextField(verbose_name="备注", default="", null=True)

    user = ForeignKey(User, on_delete=CASCADE)

    update_time = DateTimeField(verbose_name="更新时间", auto_now=True)
    create_time = DateTimeField(verbose_name="创建时间", default=timezone.now)

    class Meta:
        db_table = DB_PREFIX + "certification"
