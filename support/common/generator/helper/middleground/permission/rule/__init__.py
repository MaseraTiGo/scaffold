# coding=UTF-8

from infrastructure.utils.common.dictwrapper import DictWrapper
from support.common.generator.base import BaseGenerator
from support.common.generator.helper import PlatformGenerator
from abs.middleground.technology.permission.store import Rule


class RuleGenerator(BaseGenerator):

    def __init__(self, rule_infos):
        super(RuleGenerator, self).__init__()
        self._rule_infos = self.init(rule_infos)

    def get_create_list(self, result_mapping):
        platform_list = result_mapping.get(
            PlatformGenerator.get_key()
        )
        platform_mapping = {
            platform.name: platform
            for platform in platform_list
        }
        rule_list = []
        for rule_info in self._rule_infos:
            platform = platform_mapping.get(
                rule_info['platform_name']
            )
            if platform:
                rule_info.update({
                    "platform": platform
                })
                rule_list.append(DictWrapper(rule_info))
        return rule_list

    def create(self, rule_info, result_mapping):
        rule_qs = Rule.query().filter(
            platform=rule_info.platform,
        )
        if rule_qs.count() <= len(self._rule_infos):
            parent_id = 0
            if rule_info['parent']:
                rule_qs = Rule.query().filter(
                    name=rule_info["parent"],
                    platform=rule_info.platform,
                )
                if rule_qs.count() > 0:
                    parent_id = rule_qs[0].id
            rule_info.update({
                'parent_id': parent_id
            })
            rule_group = Rule.create(
                **rule_info
            )
        return rule_group

    def delete(self):
        print('==================>>> delete rule_group <==================')
        return None
