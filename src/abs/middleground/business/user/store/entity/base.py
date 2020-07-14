# coding=UTF-8

'''
Created on 2020年7月10日

@author: Administrator
'''

from abs.common.model import BaseModel, \
        CharField, DateTimeField, DateField, timezone
from abs.middleground.business.user.utils.constant import GenderTypes
from abs.middleground.business.user.settings import DB_PREFIX


class User(BaseModel):
    """个人信息表"""
    name = CharField(verbose_name="姓名", max_length=32)
    gender = CharField(
        verbose_name="性别",
        max_length=24,
        choices=GenderTypes.CHOICES,
        default=GenderTypes.UNKNOWN
    )
    birthday = DateField(verbose_name="生日", null=True)
    phone = CharField(verbose_name="手机号", max_length=20, default="")
    email = CharField(verbose_name="邮箱", max_length=128, default="")
    wechat = CharField(verbose_name="微信", max_length=128, default="")
    qq = CharField(verbose_name="qq", max_length=128, default="")

    update_time = DateTimeField(verbose_name="更新时间", auto_now=True)
    create_time = DateTimeField(verbose_name="创建时间", default=timezone.now)

    class Meta:
        db_table = DB_PREFIX + "base"

    @classmethod
    def search(cls, **attrs):
        user_qs = cls.query().filter(**attrs)
        return user_qs

    @classmethod
    def is_exsited(cls, phone):
        user_qs = cls.search(phone = phone)
        if user_qs.count() > 0:
            return True, user_qs[0]
        return False, None
