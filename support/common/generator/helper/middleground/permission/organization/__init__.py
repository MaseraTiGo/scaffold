# coding=UTF-8

import json
from infrastructure.utils.common.dictwrapper import DictWrapper
from support.common.generator.base import BaseGenerator
from support.common.generator.helper import AuthorizationGenerator
from abs.middleground.technology.permission.store import \
        Organization, Position


class OrganizationGenerator(BaseGenerator):

    def __init__(self, organization_info):
        super(OrganizationGenerator, self).__init__()
        self._organization_infos = self.init(organization_info)

    def get_create_list(self, result_mapping):
        authorization_list = result_mapping.get(
            AuthorizationGenerator.get_key()
        )
        result = {}
        for authorization in authorization_list:
            platform = authorization.platform
            if platform.name not in result:
                result[platform.name] = platform
                platform.company_mapping = {}
            result[platform.name].company_mapping[
                authorization.company_name
            ] = authorization

        organization_list = []
        for organization_info in self._organization_infos:
            platform = result[organization_info['platform']]
            authorization = platform.company_mapping[
                organization_info['company']
            ]
            if authorization:
                organization_info.update({
                    "authorization": authorization,
                })
                organization_list.append(DictWrapper(organization_info))
        return organization_list

    def create(self, organization_info, result_mapping):
        organization_qs = Organization.query().filter(
            name=organization_info.name,
            authorization=organization_info.authorization,
        )
        if organization_qs.count():
            organization = organization_qs[0]
        else:
            organization_info.parent_id = 0
            if organization_info.parent:
                parent = Organization.query(
                    name=organization_info.parent,
                    authorization=organization_info.authorization,
                )[0]
                organization_info.parent_id = parent.id
                position_id_list = [
                    position.id
                    for position in Position.query().filter(
                        authorization=organization_info['authorization'],
                        name__in=organization_info['position_list']
                    )
                ]
                organization_info.update({
                    'position_id_list': json.dumps(position_id_list)
                })
            organization = Organization.create(**organization_info)
        return organization

    def delete(self):
        print('==================>>> delete organization <==================')
        return None
