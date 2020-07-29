# coding=UTF-8


from infrastructure.log.base import logger
from infrastructure.utils.common.dictwrapper import DictWrapper
from support.common.generator.base import BaseGenerator

from abs.services.crm.university.models import School


class SchoolGenerator(BaseGenerator):

    def __init__(self, school_infos):
        super(SchoolGenerator, self).__init__()
        self._school_infos = self.init(school_infos)

    def get_create_list(self, result_mapping):
        return self._school_infos

    def create(self, school_info, result_mapping):
        school_qs = School.query(
            name=school_info.name,
        )
        if school_qs.count():
            school = school_qs[0]
        else:
            school = School.create(**school_info)
        return school

    def delete(self):
        logger.info('================> delete customer <==================')
        return None
