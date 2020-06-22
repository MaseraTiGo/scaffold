# coding=UTF-8

import time

from infrastructure.utils.common.single import Single
from abs.middleware.rule.entity import RuleEntity
from abs.middleware.rule.constant import permise_rules, staff_rules, product_rules, \
 communication_rules, eventonlineservice_rules, wechatmanage_rules


class RuleRegister(Single):

    def __init__(self):
        self._rule_mapping = {}
        self._root_list = []

    def register_module(self, module, *modules):
        module_list = [module]
        module_list.extend(modules)
        for module_entity in module_list:
            mapping = module_entity.get_all_mapping()
            if module_entity.root.all_key not in self._rule_mapping:
                self._root_list.append(module_entity.root)
                self._rule_mapping.update(mapping)

    def get_roots(self):
        return self._root_list

    def get_rule_mapping(self):
        return self._rule_mapping

    def register_api(self, entity, api, *apis):
        entity.add_apis(api, *apis)


rule_register = RuleRegister()
rule_register.register_module(permise_rules)
rule_register.register_module(staff_rules)
rule_register.register_module(product_rules)
rule_register.register_module(communication_rules)
rule_register.register_module(eventonlineservice_rules)
rule_register.register_module(wechatmanage_rules)
