# coding=UTF-8


import datetime
import json
from infrastructure.utils.common.dictwrapper import DictWrapper
from abs.middleground.technology.permission.manager.base import Helper, \
        Entity
from abs.middleground.technology.permission.models import \
        Organization, Position


class OrganizationEntity(Entity):

    def get_root_model(self):
        return DictWrapper({
            'id': -1,
            'name': "根节点",
            'remark': "根节点",
            'description': "根节点",
            'parent_id': -1,
            'create_time': datetime.datetime.now(),
            'update_time': datetime.datetime.now(),
        })

    def get_attr_fiels(self):
        return (
            'name',
            'remark',
            'description',
            'parent_id',
            'create_time',
            'update_time',
        )


class OrganizationHelper(Helper):

    ENTITY_CLASS = OrganizationEntity

    def __init__(self, authorization):
        self.authorization = authorization

    def get_entity_list(self):
        position_mapping = {
            position.id: position
            for position in Position.query(
                authorization=self.authorization
            )
        }
        organization_list = []
        for organization in Organization.query(
            authorization=self.authorization
        ):
            organization.position_name_list = json.dumps([
                position_mapping[position_id].name
                for position_id in json.loads(organization.position_id_list)
            ])
            organization_list.append(organization)
        return organization_list
