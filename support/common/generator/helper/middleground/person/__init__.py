# coding=UTF-8


from infrastructure.log.base import logger
from support.common.generator.base import BaseGenerator
from abs.middleground.business.person.store import Person


class PersonGenerator(BaseGenerator):

    def __init__(self, person_infos):
        super(PersonGenerator, self).__init__()
        self._person_infos = self.init(person_infos)

    def get_create_list(self, result_mapping):
        return self._person_infos

    def create(self, person_info, result_mapping):
        person_qs = Person.query().filter(phone=person_info.phone)
        if person_qs.count():
            person = person_qs[0]
        else:
            person = Person.create(**person_info)
        return person

    def delete(self):
        logger.info('=================>>> delete person <=================')
        return None
