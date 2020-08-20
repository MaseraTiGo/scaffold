# coding=UTF-8

import random
from infrastructure.utils.common.dictwrapper import DictWrapper
from support.common.generator.base import BaseGenerator
from support.common.generator.helper import AuthorizationGenerator, \
OrganizationGenerator, PositionGenerator, PersonGenerator
from abs.middleground.technology.permission.store import PositionPermission


class PersonPositionGenerator(BaseGenerator):


    def get_create_list(self, result_mapping):
        person_list = result_mapping.get(PersonGenerator.get_key())
        authorization_list = result_mapping.get(AuthorizationGenerator.get_key())
        organization_list = result_mapping.get(OrganizationGenerator.get_key())
        position_list = result_mapping.get(PositionGenerator.get_key())
        person_position_list = []
        for authorization in authorization_list:
            for person in person_list:
                if person.name == "admin":
                    organization = None
                    position = None
                    for organization in organization_list:
                        if organization.name == "公司":
                            organization = organization
                    for position in position_list:
                        if organization.name == "超级管理员":
                            position = position
                else:
                    organization = random.choice(organization_list)
                    position = random.choice(position_list)

                person_position_info = DictWrapper({
                    "person_id": person.id,
                    "authorization": authorization,
                    "organization": organization,
                    "position": position,
                })
                person_position_list.append(person_position_info)
        return person_position_list

    def create(self, person_position_info, result_mapping):
        person_position_qs = PositionPermission.query().filter(
            person_id = person_position_info.person_id,
            authorization = person_position_info.authorization,
            position = person_position_info.position
        )
        if person_position_qs.count():
            person_position = person_position_qs[0]
        else:
            person_position = PositionPermission.create(**person_position_info)
        return person_position

    def delete(self):
        print('==================>>> delete person_position <==================')
        return None
