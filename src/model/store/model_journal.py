# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''
import json

from django.db.models import *
from django.utils import timezone
from model.base import BaseModel


class JournalTypes(object):
    LOGIN = "login"
    OTHER = "other"
    DELETE = "delete"
    IMPORTRESET = "status reset"
    LOOK = "look"
    SEARCH = "search"
    EDIT = "edit"
    REMOVE = "remove"
    UPDATE = "update"
    ADD = "add"
    RECOVER = "recover"
    IMPORTDATA = "import"
    ALLOT = "allot"
    CLOSE = "close"
    CHOICES = ((LOGIN, '登录'), (OTHER, "其它"), (IMPORTRESET, "导入数据状态重置"), (DELETE, "删除"), (LOOK, "查詢"), \
               (EDIT, "編輯"), (SEARCH, "搜索"), (REMOVE, "刪除"), (UPDATE, "更新"), (ADD, "新增"), (IMPORTDATA, "数据导入"), \
               (RECOVER, "恢复"), (ALLOT, "分配"), (CLOSE, "关闭"),
               )



class OperationTypes(object):
    STAFF = "staff"
    USER = "user"
    SYSTEM = "system"
    CHOICES = ((STAFF, '员工'), (USER, "用户"), (SYSTEM, "系统"))


class Journal(BaseModel):
    """日志表"""
    active_uid = IntegerField(verbose_name = "主动方uid", default = 0)
    active_name = CharField(verbose_name = "主动方姓名", max_length = 128)
    active_type = CharField(verbose_name = "主动方类型", max_length = 64, choices = OperationTypes.CHOICES, default = OperationTypes.SYSTEM)
    passive_uid = IntegerField(verbose_name = "被动方uid", default = 0)
    passive_name = CharField(verbose_name = "被动方姓名", max_length = 128)
    passive_type = CharField(verbose_name = "被动方类型", max_length = 64, choices = OperationTypes.CHOICES, default = OperationTypes.SYSTEM)
    journal_type = CharField(verbose_name = "日志类型", max_length = 64, choices = JournalTypes.CHOICES, default = JournalTypes.OTHER)
    record_detail = TextField(verbose_name = "详情")
    remark = TextField(verbose_name = "备注")

    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)

    class Meta:
        db_table = "staff_journal"

    @classmethod
    def search(cls, **attrs):
        journal_qs = cls.query().filter(**attrs)
        return journal_qs


