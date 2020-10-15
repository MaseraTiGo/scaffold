# coding=UTF-8

import random

from abs.middleground.technology.permission.store.entity.person import PersonGroup
from abs.middleground.technology.permission.store.entity.platform import Authorization
from abs.middleground.technology.permission.store.entity.rule import RuleGroup
from infrastructure.log.base import logger
from support.common.generator.base import BaseGenerator


class PersonGroupGenerator(BaseGenerator):

    def __init__(self, person_group_infos):
        super(PersonGroupGenerator, self).__init__()
        self._person_group_infos = self.init(person_group_infos)

    def get_create_list(self, result_mapping):
        infos_list = []
        for person_gp in self._person_group_infos:
            platform_company = Authorization.search(company_name=person_gp.company_name)[0]
            rule_group_list = RuleGroup.search(authorization=platform_company)
            person_gp.update({
                'authorization': platform_company,
                'rule_group': random.choice(rule_group_list),

            })
            infos_list.append(person_gp)
        return infos_list

    def create(self, infos, result_mapping):
        infos_qs = PersonGroup.query(
            name=infos.name,
            authorization=infos.authorization,
            rule_group=infos.rule_group
        )
        if infos_qs.count():
            p_group = infos_qs[0]
        else:
            p_group = PersonGroup.create(**infos)
        return p_group

    def delete(self):
        logger.info('================> delete person group <==================')
        return None
