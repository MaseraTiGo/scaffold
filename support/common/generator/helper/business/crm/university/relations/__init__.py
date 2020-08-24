# coding=UTF-8


from infrastructure.log.base import logger
from infrastructure.utils.common.dictwrapper import DictWrapper
from support.common.generator.base import BaseGenerator
from support.common.generator.helper import SchoolGenerator, MajorGenerator

from abs.services.crm.university.models import Relations


class RelationsGenerator(BaseGenerator):

    def __init__(self, relations_infos):
        super(RelationsGenerator, self).__init__()
        self._relations_infos = self.init(relations_infos)

    def get_create_list(self, result_mapping):
        school_list = result_mapping.get(SchoolGenerator.get_key())
        major_list = result_mapping.get(MajorGenerator.get_key())
        relations_list = []
        if self._relations_infos:
            for relations_info in self._relations_infos:
                school_fiter = list(filter(
                    lambda obj: obj.name == relations_info.school_name,
                    school_list
                ))
                major_fiter = list(filter(
                    lambda obj: obj.name == relations_info.major_name,
                    major_list
                ))
                if school_fiter and major_fiter:
                    school = school_fiter[0]
                    major = major_fiter[0]
                    relations_info = {
                        "school":school,
                        "major":major
                    }
                    relations_list.append(DictWrapper(relations_info))
        else:
            for school in school_list:
                for major in major_list:
                    relations_info = {
                        "school":school,
                        "major":major
                    }
                    relations_list.append(DictWrapper(relations_info))
        return relations_list

    def create(self, relations_info, result_mapping):
        relations_qs = Relations.query(
            school = relations_info.school,
            major = relations_info.major,
        )
        if relations_qs.count():
            relations = relations_qs[0]
        else:
            relations = Relations.create(**relations_info)
        return relations

    def delete(self):
        logger.info('================> delete relations <==================')
        return None
