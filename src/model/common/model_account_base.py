# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

from django.db.models import *
from django.utils import timezone
from model.base import BaseModel


class StatusTypes(object):
    ENABLE = 'enable'
    LOCK = 'lock'
    DISABLE = 'disable'
    NOTACTIVE = 'notactive'

    CHOICES = ((ENABLE, '启用'), (NOTACTIVE, '待激活'), (LOCK, "锁定"), (DISABLE, "禁用"))


class BaseAccount(BaseModel):
    """基础账号表"""
    username = CharField(verbose_name = "账号", max_length = 64)
    password = CharField(verbose_name = "密码", max_length = 64)
    last_login_time = DateTimeField(verbose_name = "最后一次登录时间", null = True, blank = True)
    last_login_ip = CharField(verbose_name = "最后一次登录ip", max_length = 64, default = '')
    register_ip = CharField(verbose_name = "注册IP", max_length = 64, default = '')
    status = CharField(verbose_name = "账号状态", max_length = 64, choices = StatusTypes.CHOICES,
                       default = StatusTypes.NOTACTIVE)

    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)

    class Meta:
        abstract = True

    @classmethod
    def get_account_byusername(cls, username):
        """ 根据用户名查询账号信息 """
        try:
            return cls.objects.filter(username = username)[0]
        except:
            return None
