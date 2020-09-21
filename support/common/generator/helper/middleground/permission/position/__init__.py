# coding=UTF-8

from infrastructure.utils.common.dictwrapper import DictWrapper
from support.common.generator.base import BaseGenerator
from support.common.generator.helper import AuthorizationGenerator
from abs.middleground.technology.permission.store import Position,\
        RuleGroup


class PositionGenerator(BaseGenerator):

    def __init__(self, position_info):
        super(PositionGenerator, self).__init__()
        self._position_infos = self.init(position_info)

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
        position_list = []
        for position_info in self._position_infos:
            platform = result[position_info['platform']]
            authorization = platform.company_mapping[
                position_info['company']
            ]
            if authorization:
                position_info.update({
                    "authorization": authorization,
                })
                position_list.append(DictWrapper(position_info))
        return position_list

    def create(self, position_info, result_mapping):
        position_qs = Position.query().filter(
            name=position_info.name,
            authorization=position_info.authorization
        )
        if position_qs.count():
            position = position_qs[0]
        else:
            position_info.parent_id = 0
            if position_info.parent:
                parent = Position.query(
                    name=position_info.parent,
                    authorization=position_info.authorization
                )[0]
                position_info.parent_id = parent.id
            rule_group_qs = RuleGroup.query(
                name=position_info['rule_group'],
                authorization=position_info['authorization']
            )
            if rule_group_qs.count() > 0:
                position_info.update({"rule_group": rule_group_qs[0]})
                position = Position.create(**position_info)
        return position

    def delete(self):
        print('==================>>> delete position <==================')
        return None
