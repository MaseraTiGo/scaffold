# coding=UTF-8

from infrastructure.utils.common.dictwrapper import DictWrapper
from support.common.generator.base import BaseGenerator
from support.common.generator.helper import AuthorizationGenerator
from abs.middleground.technology.permission.store import Organization


class OrganizationGenerator(BaseGenerator):

    def __init__(self, organization_info):
        super(OrganizationGenerator, self).__init__()
        self._organization_infos = self.init(organization_info)

    def get_create_list(self, result_mapping):
        authorization_list = result_mapping.get(AuthorizationGenerator.get_key())
        organization_list = []
        for authorization in authorization_list:
            for organization_info in self._organization_infos:
                organization = organization_info.copy()
                organization.update({
                    "authorization":authorization
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
