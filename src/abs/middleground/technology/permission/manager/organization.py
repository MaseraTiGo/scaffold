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
            'position_id_list': "[]",
            'position_list': [],
            'create_time': datetime.datetime.now(),
            'update_time': datetime.datetime.now(),
        })

    def get_attr_fiels(self):
        return (
            'name',
            'remark',
            'description',
            'parent_id',
            'position_id_list',
            'position_list',
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
            remove_list = []
            position_id_list = json.loads(
                organization.position_id_list
            )
            organization.position_list = []
            for position_id in position_id_list:
                if position_id in position_mapping:
                    position = position_mapping[position_id]
                    organization.position_list.append(
                        {
                            "id": position.id,
                            "name": position.name,
                        }
                    )
                else:
                    remove_list.append(position_id)
            organization_list.append(organization)
            if remove_list:
                new_id_list = list(
                    set(position_id_list) - set(remove_list)
                )
                organization.update(
                    position_id_list=json.dumps(new_id_list)
                )

        return organization_list
