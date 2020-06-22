# coding=UTF-8

import json
from model.store.model_staff import Role
from abs.middleware.rule import rule_register
from support.generator.base import BaseGenerator


class RoleGenerator(BaseGenerator):

    def __init__(self, role_info):
        super(RoleGenerator, self).__init__()
        self._role_infos = self.init(role_info)

    def get_create_list(self, result_mapping):
        rule_list = list(rule_register.get_rule_mapping().keys())
        rules = json.dumps(rule_list)
        rules = json.dumps([])
        role_list = []
        for role_info in self._role_infos:
            role_info.rules = rules
            role_list.append(role_info)
        return role_list

    def create(self, role_info, result_mapping):
        role_qs = Role.query().filter(name = role_info.name)
        if role_qs.count():
            role = role_qs[0]
        else:
            if role_info.parent:
                parent = Role.query(name = role_info.parent)[0]
                role_info.parent_id = parent.id
            else:
                role_info.parent_id = 0
            role = Role.create(**role_info)
        return role

    def delete(self):
        print('======================>>> delete role <======================')
        return None
