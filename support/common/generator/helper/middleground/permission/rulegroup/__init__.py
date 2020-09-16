# coding=UTF-8

import json
from infrastructure.utils.common.dictwrapper import DictWrapper
from support.common.generator.base import BaseGenerator
from support.common.generator.helper import AuthorizationGenerator
from abs.middleground.technology.permission.store import \
        RuleGroup, Rule


class RuleGroupGenerator(BaseGenerator):

    def __init__(self, rule_group_infos):
        super(RuleGroupGenerator, self).__init__()
        self._rule_group_infos = self.init(rule_group_infos)

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

        rule_group_list = []
        for rule_group_info in self._rule_group_infos:
            platform = result[rule_group_info['platform']]
            authorization = platform.company_mapping[
                rule_group_info['company']
            ]
            if platform and authorization:
                rule_group_info.update({
                    "platform": platform,
                    "authorization": authorization
                })
                rule_group_list.append(DictWrapper(rule_group_info))
        return rule_group_list

    def create(self, rule_group_info, result_mapping):
        rule_group_qs = RuleGroup.query().filter(
            name=rule_group_info.name,
            authorization=rule_group_info.authorization,
        )
        if rule_group_qs.count():
            rule_group = rule_group_qs[0]
        else:
            content = rule_group_info.pop('content')
            rule_list = []
            for item in json.loads(content):
                sub_rule_list = item.split("-")
                sub_rule = []
                parent_id = 0
                for name in sub_rule_list:
                    rule_qs = Rule.query().filter(
                        name=name,
                        parent_id=parent_id
                    )
                    if rule_qs.count():
                        rule = rule_qs[0]
                        sub_rule.append(rule.code)
                        parent_id = rule.id
                rule_list.append('-'.join(sub_rule))

            rule_group = RuleGroup.create(
                content=json.dumps(rule_list),
                **rule_group_info
            )
        return rule_group

    def delete(self):
        print('==================>>> delete rule_group <==================')
        return None
