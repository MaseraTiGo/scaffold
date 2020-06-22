# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''
import json

from django.db.models import *
from django.utils import timezone
from model.base import BaseModel
from model.common.model_user_base import UserCertification
from model.common.model_account_base import BaseAccount


class Staff(BaseModel):
    """员工表"""
    id_number = CharField(verbose_name = "员工工号", max_length = 128)
    certification = ForeignKey(UserCertification, on_delete=DO_NOTHING)
    entry_time = DateField(verbose_name = "入职时间", null = True, blank = True)
    resignation_time = DateField(verbose_name = "离职时间", null = True, blank = True)
    is_admin = BooleanField(verbose_name = "是否是管理员", default = False)

    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)

    class Meta:
        db_table = "staff_info"

    @property
    def department_role_list(self):
        return DepartmentRole.get_all_bystaff(self)

    @classmethod
    def get_staff_byname(cls, name):
        """根据姓名查询员工"""
        try:
            return cls.query().filter(name = name)[0]
        except:
            return None

    @classmethod
    def search(cls, **attrs):
        staff_qs = cls.query().filter(**attrs)
        return staff_qs

    @classmethod
    def create(cls, **infos):
        staff = cls.create(**infos)
        if staff is not None:
             number = "BQ{number}".format(number = (staff.id + 10000))
             staff.update(number = number)

        return staff

    def update(self, **infos):
        certification = self.certification.update(**infos)
        if certification:
            super(Staff, self).update(certification = certification, **infos)
            return self
        else:
            return None


class Account(BaseAccount):
    """员工账号表"""
    staff = ForeignKey(Staff, on_delete=CASCADE)

    class Meta:
        db_table = "staff_account"

    @classmethod
    def is_exsited(cls, username, password):
        account_qs = cls.objects.filter(username = username, password = password)
        if account_qs.count():
            return True, account_qs[0]
        return False, None

    @classmethod
    def get_account_bystaff(cls, staff_id):
        """根据staff_id查询账号信息"""
        try:
            return cls.objects.filter(staff = staff_id)[0]
        except:
            return None


class DataLevelTypes(object):
    ONLY_SELF = 'only_self'
    SELF_AND_SUBORDINATE = 'self_and_subordinate'
    ALL = 'all'

    CHOICES = ((ONLY_SELF, '仅自己可见数据'), (SELF_AND_SUBORDINATE, '自己及下属'), (ALL, "所有"))


class Role(BaseModel):
    name = CharField(verbose_name = "角色名称", max_length = 64, default = "")
    describe = TextField(verbose_name = "描述", default = "")
    parent_id = IntegerField(verbose_name = "对应上级角色id", default = 0)
    rules = TextField(verbose_name = "角色对应权限", default = "[]")
    data_level= CharField(verbose_name = "数据展现级别", max_length = 24, choices =
                          DataLevelTypes.CHOICES)
    data_security = BooleanField(verbose_name = "数据级别", default = True)

    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)

    class Meta:
        db_table = "staff_role"

    @classmethod
    def search(cls, **attrs):
        role_qs = cls.query().filter(**attrs)
        return role_qs

    @property
    def rule_list(self):
        try:
            return json.loads(self.rules)
        except Exception as e:
            print(e)
            return []


class Department(BaseModel):
    name = CharField(verbose_name = "部门名称", max_length = 64, default = "")
    parent_id = IntegerField(verbose_name = "对应上级部门id", default = 0)
    describe = TextField(verbose_name = "描述", default = "")

    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)

    class Meta:
        db_table = "staff_department"

    @classmethod
    def search(cls, **attrs):
        department_qs = cls.query().filter(**attrs)
        return department_qs


class DepartmentRole(BaseModel):
    staff = ForeignKey(Staff, on_delete=CASCADE)
    role = ForeignKey(Role, on_delete=CASCADE)
    department = ForeignKey(Department, on_delete=CASCADE)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)

    class Meta:
        db_table = "staff_department_role"

    @classmethod
    def get_all_bystaff(cls, staff):
        return cls.query(staff = staff)


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

