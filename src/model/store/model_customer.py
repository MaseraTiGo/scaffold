# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''
import json

from django.db.models import *
from django.utils import timezone
from model.base import BaseModel
from model.common.model_user_base import GenderTypes, EducationType, UserCertification
from model.common.model_account_base import BaseAccount


class Customer(BaseModel):
    """客户表"""
    name = CharField(verbose_name = "姓名", max_length = 32)
    gender = CharField(verbose_name = "性别", max_length = 24, choices = GenderTypes.CHOICES, default = GenderTypes.UNKNOWN)
    birthday = DateField(verbose_name = "生日", null = True, blank = True)
    education = CharField(verbose_name = "学历", max_length = 24, choices = EducationType.CHOICES, default = EducationType.OTHER)

    phone = CharField(verbose_name = "手机号", max_length = 20, default = "" , null = True)
    email = CharField(verbose_name = "邮箱", max_length = 128, default = "", null = True)
    wechat = CharField(verbose_name = "微信", max_length = 128, default = "", null = True)
    qq = CharField(verbose_name = "qq", max_length = 128, default = "", null = True)
    certification = ForeignKey(UserCertification, on_delete=DO_NOTHING)

    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)

    class Meta:
        db_table = "customer_info"

    @property
    def department_role_list(self):
        return DepartmentRole.get_all_bycustomer(self)

    @classmethod
    def get_customer_byname(cls, name):
        """根据姓名查询客户"""
        try:
            return cls.query().filter(name = name)[0]
        except:
            return None

    @classmethod
    def search(cls, **attrs):
        customer_qs = cls.query().filter(**attrs)
        return customer_qs

    def update(self, **infos):
        certification = self.certification.update(**infos)
        if certification:
            super(Customer, self).update(certification = certification, **infos)
            return self
        else:
            return None


class CustomerAccount(BaseAccount):
    """客户账号表"""
    nick = CharField(verbose_name = "昵称", max_length = 64)
    profile = CharField(verbose_name = "头像", max_length = 256)
    customer = ForeignKey(Customer, on_delete=CASCADE)

    class Meta:
        db_table = "customer_account"

    @classmethod
    def is_exsited(cls, username, password):
        account_qs = cls.objects.filter(username = username, password = password)
        if account_qs.count():
            return True, account_qs[0]
        return False, None

    @classmethod
    def get_account_bycustomer(cls, customer_id):
        """根据customer_id查询账号信息"""
        try:
            return cls.objects.filter(customer = customer_id)[0]
        except:
            return None
