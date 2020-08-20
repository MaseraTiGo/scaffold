# coding=UTF-8

import random
from infrastructure.utils.common.dictwrapper import DictWrapper
from support.common.generator.base import BaseGenerator
from support.common.generator.helper import AuthorizationGenerator, \
OrganizationGenerator, RuleGroupGenerator
from abs.middleground.technology.permission.store import Position


class PositionGenerator(BaseGenerator):

    def __init__(self, position_info):
        super(PositionGenerator, self).__init__()
        self._position_infos = self.init(position_info)

    def get_create_list(self, result_mapping):
        authorization_list = result_mapping.get(AuthorizationGenerator.get_key())
        organization_list = result_mapping.get(OrganizationGenerator.get_key())
        rule_group_list = result_mapping.get(RuleGroupGenerator.get_key())
        position_list = []
        for authorization in authorization_list:
            for position_info in self._position_infos:
                position = position_info.copy()
                organization_fiter = list(filter(
                    lambda obj: obj.name == position["organization"],
                    organization_list
                ))
                if organization_fiter:
                    organization = organization_fiter[0]
                    position.update({
                        "organization":organization,
                        "authorization":authorization,
                        "rule_group":random.choice(rule_group_list)
                    })
                    position_list.append(DictWrapper(position))
        return position_list

    def create(self, position_info, result_mapping):
        position_qs = Position.query().filter(
            name = position_info.name,
            authorization = position_info.authorization
        )
        if position_qs.count():
            position = position_qs[0]
        else:
            if position_info.parent:
                position = Position.query(
                    name = position_info.parent,
                    authorization = position_info.authorization
                )[0]
                position_info.parent_id = parent.id
            else:
                position_info.parent_id = 0
            position = Position.create(**position_info)
        return position

    def delete(self):
        print('==================>>> delete position <==================')
        return None
