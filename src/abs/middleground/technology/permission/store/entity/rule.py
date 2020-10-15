# coding=UTF-8

'''
Created on 2020年7月10日

@author: Administrator
'''

import random
from abs.common.model import BaseModel, ForeignKey, CASCADE,\
        IntegerField, CharField, DateTimeField, TextField, timezone
from abs.middleground.technology.permission.settings import DB_PREFIX
from abs.middleground.technology.permission.store.entity.platform import \
        PlatForm, Authorization


class Rule(BaseModel):
    """
    权限
    """
    name = CharField(verbose_name="权限名称", max_length=32)
    description = TextField(verbose_name="描述")
    code = CharField(verbose_name="权限编码", max_length=128)
    parent_id = IntegerField(verbose_name="上级权限", default=0)
    remark = TextField(verbose_name="备注")

    platform = ForeignKey(PlatForm, on_delete=CASCADE)
    update_time = DateTimeField(verbose_name="更新时间", auto_now=True)
    create_time = DateTimeField(verbose_name="创建时间", default=timezone.now)

    class Meta:
        db_table = DB_PREFIX + "rule"

    @classmethod
    def generate_code(cls):
        char_up_list = [chr(i) for i in range(65, 90)]
        char_low_list = [chr(i) for i in range(97, 122)]
        char_list = char_up_list + char_low_list
        code = ''.join(random.choice(char_list) for _ in range(4))
        return code

    @classmethod
    def create(cls, **rule_info):
        # if code not in rule info then it should be generated. --- modified by djd
        if 'code' not in rule_info:
            rule_info.update({'code': cls.generate_code()})
        return super(Rule, cls).create(
            **rule_info
        )

    def get_children(self):
        rule_qs = self.query().filter(
            parent_id=self.id
        )
        return list(rule_qs)


class RuleGroup(BaseModel):
    """
    权限组
    content:
        [
            {
                name: xxxx
                code: A
                children: [
                    {
                        name: xxxx
                        code: B
                        children: [
                            .....

                        ]
                    },
                    .....
                ]
            },
            .....
        ]
    注：叶子节点即为操作项
    """
    name = CharField(verbose_name="权限组名称", max_length=32)
    description = TextField(verbose_name="描述")
    remark = TextField(verbose_name="备注")
    content = TextField(verbose_name="权限内容")

    authorization = ForeignKey(Authorization, on_delete=CASCADE)
    update_time = DateTimeField(verbose_name="更新时间", auto_now=True)
    create_time = DateTimeField(verbose_name="创建时间", default=timezone.now)

    class Meta:
        db_table = DB_PREFIX + "rulegroup"
