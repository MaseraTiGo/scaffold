# coding=UTF-8


from abs.middleground.technology.permission.manager.base import Helper, \
        Entity
from abs.middleground.technology.permission.models import Organization


class OrganizationEntity(Entity):

    def get_attr_fiels(self):
        return ('name', 'remark', 'description', 'parent_id', 'create_time')


class OrganizationHelper(Helper):

    ENTITY_CLASS = OrganizationEntity

    def __init__(self, platform):
        self.platform = platform

    def get_entity_list(self):
        return Organization.query(
            platform=self.platform
        )
