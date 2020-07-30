# coding=UTF-8


from abs.middleground.technology.permission.manager.base import Helper, \
        Entity
from abs.middleground.technology.permission.models import Rule


class RuleEntity(Entity):

    def get_attr_fiels(self):
        return ('name', 'code')


class RuleHelper(Helper):

    ENTITY_CLASS = RuleEntity

    def __init__(self, platform):
        self.platform = platform

    def get_entity_list(self):
        return Rule.query(
            platform=self.platform
        )
