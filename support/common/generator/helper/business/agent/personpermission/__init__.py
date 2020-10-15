# coding=UTF-8

import random

from abs.middleground.business.person.store.entity.base import Person
from abs.middleground.technology.permission.store.entity.person import PersonPermission
from infrastructure.log.base import logger
from support.common.generator.base import BaseGenerator
from support.common.generator.helper.business.crm.persongroup import PersonGroupGenerator


class PersonPermissionGenerator(BaseGenerator):

    def __init__(self, person_infos):
        super(PersonPermissionGenerator, self).__init__()
        self._person_infos = self.init(person_infos)

    def get_create_list(self, result_mapping):
        infos_list = []
        for person in self._person_infos:
            person_id = Person.search(phone=person.phone)[0].id
            person_group_list = result_mapping.get(PersonGroupGenerator.get_key())
            person_group = random.choice(person_group_list)
            person.update({
                'authorization': person_group.authorization,
                'person_group': person_group,
                'person_id': person_id

            })
            infos_list.append(person)
        return infos_list

    def create(self, infos, result_mapping):
        # todo
        infos_qs = PersonPermission.query(
            person_id=infos.person_id
        )
        if infos_qs.count():
            permission = infos_qs[0]
        else:
            permission = PersonPermission.create(**infos)
        return permission

    def delete(self):
        logger.info('================> delete person permission <==================')
        return None
