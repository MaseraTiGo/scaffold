# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

from django.db.models import *
from django.utils import timezone
from model.base import BaseModel


class GenderTypes(object):
    MAN = "man"
    WOMAN = "woman"
    UNKNOWN = "unknown"
    CHOICES = ((MAN, '男士'), (WOMAN, "女士"), (UNKNOWN, "未知"))


class EducationType(object):
    PRIMARY = "primary"
    MIDDLE = "middle"
    HIGH = "high"
    UNDERGRADUAYE = "undergraduate"
    COLLEGE = "college"
    MIDDLECOLLEGE = "middlecollege"
    MASTER = "master"
    DOCTOR = "doctor"
    OTHER = "other"
    CHOICES = ((PRIMARY, '小学'), (MIDDLE, "初中"), (HIGH, "高中"), (UNDERGRADUAYE, "本科"), (COLLEGE, "大专"), \
               (MIDDLECOLLEGE, "中专"), (MASTER, "硕士"), (DOCTOR, "博士"), (OTHER, "其他"))


class UserCertification(BaseModel):
    name = CharField(verbose_name = "姓名", max_length = 64)
    identification = CharField(verbose_name = "身份证号", max_length = 24)
    id_front = CharField(verbose_name = "身份证正面", max_length = 256, default = "", null = True)
    id_back = CharField(verbose_name = "身份证反面", max_length = 256, default = "", null = True)
    id_in_hand = CharField(verbose_name = "身份证反面", max_length = 256, default = "", null = True)
    remark = TextField(verbose_name = "备注", default = "", null = True)

    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)


    class Meta:
        db_table = "user_certification"
