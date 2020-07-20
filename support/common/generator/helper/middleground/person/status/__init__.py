# coding=UTF-8


from infrastructure.log.base import logger
from infrastructure.utils.common.dictwrapper import DictWrapper
from support.common.generator.base import BaseGenerator
from support.common.generator.helper import PersonGenerator
from abs.middleground.business.person.store import PersonStatus


class StatusGenerator(BaseGenerator):

    def get_create_list(self, result_mapping):
        person_list = result_mapping.get(PersonGenerator.get_key())
        status_list = []
        for person in person_list:
            status_info = DictWrapper({
                'person': person
            })
            status_list.append(status_info)
        return status_list

    def create(self, status_info, result_mapping):
        status_qs = PersonStatus.query().filter(
            person=status_info.person
        )
        if status_qs.count():
            status = status_qs[0]
        else:
            status = PersonStatus.create(**status_info)
        return status

    def delete(self):
        logger.info('==================>>> delete person <==================')
        return None
