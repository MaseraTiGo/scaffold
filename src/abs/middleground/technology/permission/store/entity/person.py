# coding=UTF-8

'''
Created on 2020年7月10日

@author: Administrator
'''

from abs.common.model import BaseModel, ForeignKey, CASCADE,\
        CharField, IntegerField, DateTimeField, TextField, timezone
from abs.middleground.technology.permission.settings import DB_PREFIX
from abs.middleground.technology.permission.store.entity.platform import \
        Authorization
from abs.middleground.technology.permission.store.entity.rule import \
        RuleGroup


class PersonGroup(BaseModel):
    """
    用户组
    """
    name = CharField(verbose_name="权限组名称", max_length=32)
    description = TextField(verbose_name="描述")
    remark = TextField(verbose_name="备注")

    authorization = ForeignKey(Authorization, on_delete=CASCADE)
    rule_group = ForeignKey(RuleGroup, on_delete=CASCADE)
    update_time = DateTimeField(verbose_name="更新时间", auto_now=True)
    create_time = DateTimeField(verbose_name="创建时间", default=timezone.now)

    class Meta:
        db_table = DB_PREFIX + "person_group"


class PersonPermission(BaseModel):
    """
    用户权限
    """
    person_id = IntegerField(verbose_name="用户id")
    person_group = ForeignKey(PersonGroup, on_delete=CASCADE)
    authorization = ForeignKey(Authorization, on_delete=CASCADE)
    create_time = DateTimeField(verbose_name="创建时间", default=timezone.now)

    class Meta:
        db_table = DB_PREFIX + "person_permission"
        unique_together = (
            ('person_id', 'authorization')
        )

    @classmethod
    def get_byperson(cls, authorization, person_id):
        pp_qs = cls.query(
            authorization=authorization,
            person_id=person_id
        )
        if pp_qs.count() > 0:
            return pp_qs[0]
        return None
