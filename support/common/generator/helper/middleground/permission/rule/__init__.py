# coding=UTF-8

from infrastructure.utils.common.dictwrapper import DictWrapper
from support.common.generator.base import BaseGenerator
from support.common.generator.helper import AuthorizationGenerator
from abs.middleground.technology.permission.store import RuleGroup


class RuleGroupGenerator(BaseGenerator):

    def __init__(self, rule_group_infos):
        super(RuleGroupGenerator, self).__init__()
        self._rule_group_infos = self.init(rule_group_infos)

    def get_create_list(self, result_mapping):
        authorization_list = result_mapping.get(AuthorizationGenerator.get_key())
        rule_group_list = []
        for authorization in authorization_list:
            for rule_group_info in self._rule_group_infos:
                rule_group = rule_group_info.copy()
                rule_group.update({
                    "authorization":authorization
                })
                rule_group_list.append(DictWrapper(rule_group))
        return rule_group_list

    def create(self, rule_group_info, result_mapping):
        rule_group_qs = RuleGroup.query().filter(
            name = rule_group_info.name,
            authorization = rule_group_info.authorization,
        )
        if rule_group_qs.count():
            rule_group = rule_group_qs[0]
        else:
            rule_group = RuleGroup.create(**rule_group_info)
        return rule_group

    def delete(self):
        print('==================>>> delete rule_group <==================')
        return None
