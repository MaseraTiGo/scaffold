# coding=UTF-8


from infrastructure.log.base import logger
from infrastructure.utils.common.dictwrapper import DictWrapper
from support.common.generator.base import BaseGenerator

from abs.services.crm.university.models import Major


class MajorGenerator(BaseGenerator):

    def __init__(self, major_infos):
        super(MajorGenerator, self).__init__()
        self._major_infos = self.init(major_infos)

    def get_create_list(self, result_mapping):
        return self._major_infos

    def create(self, major_info, result_mapping):
        major_qs = Major.search(
            name = major_info.name,
        )
        if major_qs.count():
            major = major_qs[0]
        else:
            major = Major.create(**major_info)
        return major

    def delete(self):
        logger.info('================> delete customer <==================')
        return None
