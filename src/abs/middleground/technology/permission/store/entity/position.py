# coding=UTF-8

'''
Created on 2020年7月10日

@author: Administrator
'''

from abs.common.model import BaseModel, IntegerField, CASCADE,\
        CharField, DateTimeField, ForeignKey, TextField, timezone
from abs.middleground.technology.permission.settings import DB_PREFIX
from abs.middleground.technology.permission.store.entity.platform import \
        Authorization
from abs.middleground.technology.permission.store.entity.rule import \
        RuleGroup


class Position(BaseModel):
    """
    身份（职位）
    """
    name = CharField(verbose_name="身份名称", max_length=32)
    parent_id = IntegerField(verbose_name="上级身份", default=0)
    description = TextField(verbose_name="描述")
    remark = TextField(verbose_name="备注")

    authorization = ForeignKey(Authorization, on_delete=CASCADE)
    rule_group = ForeignKey(RuleGroup, null=True, on_delete=CASCADE)
    update_time = DateTimeField(verbose_name="更新时间", auto_now=True)
    create_time = DateTimeField(verbose_name="创建时间", default=timezone.now)

    class Meta:
        db_table = DB_PREFIX + "position"

    def get_children(self):
        cls_qs = self.search(parent_id=self.id)
        return cls_qs


class Organization(BaseModel):
    """
    组织
    """
    name = CharField(verbose_name="权限名称", max_length=32)
    description = TextField(verbose_name="描述")
    parent_id = IntegerField(verbose_name="上级组织", default=0)
    remark = TextField(verbose_name="备注")

    position_id_list = TextField(verbose_name="身份列表", default="[]")  # 身份列表
    authorization = ForeignKey(Authorization, on_delete=CASCADE)
    update_time = DateTimeField(verbose_name="更新时间", auto_now=True)
    create_time = DateTimeField(verbose_name="创建时间", default=timezone.now)

    class Meta:
        db_table = DB_PREFIX + "organization"


class PositionPermission(BaseModel):
    """
    身份权限
    """
    person_id = IntegerField(verbose_name="用户id")
    authorization = ForeignKey(Authorization, on_delete=CASCADE)
    organization = ForeignKey(Organization, on_delete=CASCADE)
    position = ForeignKey(Position, on_delete=CASCADE)
    update_time = DateTimeField(verbose_name="更新时间", auto_now=True)
    create_time = DateTimeField(verbose_name="创建时间", default=timezone.now)

    class Meta:
        db_table = DB_PREFIX + "position_permission"
        unique_together = (
            ('person_id', 'authorization')
        )

    @classmethod
    def get_byposition(cls, authorization, person_id):
        pp_qs = cls.query().filter(
            authorization=authorization,
            person_id=person_id,
        )
        if pp_qs.count() > 0:
            return pp_qs[0]
        return None
