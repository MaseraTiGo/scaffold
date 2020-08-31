# coding=UTF-8


import datetime
from infrastructure.utils.common.dictwrapper import DictWrapper
from abs.middleground.technology.permission.manager.base import Helper, \
        Entity
from abs.middleground.technology.permission.models import Rule


class RuleEntity(Entity):

    def get_root_model(self):
        return DictWrapper({
            'id': -1,
            'name': "根节点",
            'remark': "根节点",
            'description': "根节点",
            'code': "",
            'parent_id': None,
            'platform_id': -1,
            'create_time': datetime.datetime.now(),
            'update_time': datetime.datetime.now(),
        })

    def get_attr_fiels(self):
        return (
            'id',
            'platform_id',
            'name',
            'code',
            'parent_id',
            'remark',
            'description',
            'create_time',
            'update_time',
        )


class RuleHelper(Helper):

    ENTITY_CLASS = RuleEntity

    def __init__(self, platform):
        self.platform = platform

    def get_entity_list(self):
        return Rule.query(
            platform=self.platform
        )
