# coding=UTF-8

from infrastructure.utils.common.dictwrapper import DictWrapper
from support.common.generator.base import BaseGenerator
from support.common.generator.helper import PlatformGenerator
from abs.middleground.technology.permission.store import RuleGroup


class RuleGroupGenerator(BaseGenerator):

    def __init__(self, rule_group_infos):
        super(RuleGroupGenerator, self).__init__()
        self._rule_group_infos = self.init(rule_group_infos)

    def get_create_list(self, result_mapping):
        platform_list = result_mapping.get(PlatformGenerator.get_key())
        rule_group_list = []
        for platform in platform_list:
            for rule_group_info in self._rule_group_infos:
                rule_group = rule_group_info.copy()
                rule_group.update({
                    "platform":platform
                })
                rule_group_list.append(DictWrapper(rule_group))
        return rule_group_list

    def create(self, rule_group_info, result_mapping):
        rule_group_qs = RuleGroup.query().filter(
            name = rule_group_info.name,
            platform = rule_group_info.platform,
        )
        if rule_group_qs.count():
            rule_group = rule_group_qs[0]
        else:
            rule_group = RuleGroup.create(**rule_group_info)
        return rule_group

    def delete(self):
        print('==================>>> delete rule_group <==================')
        return None
