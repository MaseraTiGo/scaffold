# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

from django.db.models import *
from django.utils import timezone
from model.base import BaseModel
from model.store.model_staff import Staff, Department


class EventBase(BaseModel):
    """事件基类表"""
    staff = ForeignKey(Staff, on_delete = CASCADE, null = True)
    department = ForeignKey(Department, on_delete = CASCADE, null = True)
    remark = TextField(verbose_name = "备注", null = True, default = "")

    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)

    class Meta:
        abstract = True
