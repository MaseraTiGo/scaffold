# coding=UTF-8

'''
Created on 2020年7月10日

@author: Administrator
'''

from abs.common.model import CASCADE,\
        BaseModel, ForeignKey, DateTimeField, timezone
from abs.middleground.business.user.settings import DB_PREFIX
from abs.middleground.business.user.store.entity.base import User


class UserStatistics(BaseModel):

    user = ForeignKey(User, on_delete=CASCADE)
    update_time = DateTimeField(verbose_name="更新时间", auto_now=True)
    create_time = DateTimeField(verbose_name="创建时间", default=timezone.now)

    class Meta:
        db_table = DB_PREFIX + "statistics"
