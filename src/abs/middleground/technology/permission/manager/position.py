# coding=UTF-8


import datetime
from infrastructure.utils.common.dictwrapper import DictWrapper
from abs.middleground.technology.permission.manager.base import Helper, \
        Entity
from abs.middleground.technology.permission.models import Position


class PositionEntity(Entity):

    def get_root_model(self):
        return DictWrapper({
            'id': -1,
            'name': "根节点",
            'remark': "根节点",
            'description': "根节点",
            'parent_id': -1,
            'rule_group_id': -1,
            'rule_group.name': "",
            'create_time': datetime.datetime.now(),
            'update_time': datetime.datetime.now(),
        })

    def get_attr_fiels(self):
        return (
            'name',
            'remark',
            'description',
            'parent_id',
            'rule_group_id',
            ('rule_group.name', "rule_group_name"),  # 解析名称，转换名称
            'create_time',
            'update_time'
        )


class PositionHelper(Helper):

    ENTITY_CLASS = PositionEntity

    def __init__(self, authorization):
        self.authorization = authorization

    def get_entity_list(self):
        return Position.query(
            authorization=self.authorization
        )
