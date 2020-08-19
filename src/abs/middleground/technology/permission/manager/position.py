# coding=UTF-8


from abs.middleground.technology.permission.manager.base import Helper, \
        Entity
from abs.middleground.technology.permission.models import Position


class PositionEntity(Entity):

    def get_attr_fiels(self):
        return (
            'name',
            'remark',
            'description',
            'parent_id',
            'organization_id',
            'rule_group_id',
            'create_time'
        )


class PositionHelper(Helper):

    ENTITY_CLASS = PositionEntity

    def __init__(self, authorization):
        self.authorization = authorization

    def get_entity_list(self):
        return Position.query(
            authorization=self.authorization
        )
