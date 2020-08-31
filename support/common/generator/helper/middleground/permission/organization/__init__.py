# coding=UTF-8
import json
from infrastructure.utils.common.dictwrapper import DictWrapper
from support.common.generator.base import BaseGenerator
from support.common.generator.helper import AuthorizationGenerator, \
     PositionGenerator
from abs.middleground.technology.permission.store import Organization


class OrganizationGenerator(BaseGenerator):

    def __init__(self, organization_info):
        super(OrganizationGenerator, self).__init__()
        self._organization_infos = self.init(organization_info)

    def get_create_list(self, result_mapping):
        authorization_list = result_mapping.get(AuthorizationGenerator.get_key())
        position_list = result_mapping.get(PositionGenerator.get_key())
        organization_list = []
        for authorization in authorization_list:
            for organization_info in self._organization_infos:
                organization = organization_info.copy()
                position_id_list = []
                if 'position_name_list' in organization:
                    position_name_list = organization.pop("position_name_list")
                    for position_name in position_name_list:
                        position_fiter = list(filter(
                            lambda obj: obj.name == position_name and \
                                        obj.authorization == authorization,
                            position_list
                        ))
                        if position_fiter:
                            position = position_fiter[0]
                            if position.id not in position_id_list:
                                position_id_list.append(position.id)
                organization.update({
                    "authorization":authorization,
                    "position_id_list":json.dumps(position_id_list)
                })
                organization_list.append(DictWrapper(organization))
        return organization_list

    def create(self, organization_info, result_mapping):
        organization_qs = Organization.query().filter(
            name = organization_info.name,
            authorization = organization_info.authorization,
        )
        if organization_qs.count():
            organization = organization_qs[0]
        else:
            if organization_info.parent:
                organization = Organization.query(
                    name = organization_info.parent,
                    authorization = organization_info.authorization,
                )[0]
                organization_info.parent_id = parent.id
            else:
                organization_info.parent_id = 0
            organization = Organization.create(**organization_info)
        return organization

    def delete(self):
        print('==================>>> delete organization <==================')
        return None
