# coding=UTF-8


from infrastructure.log.base import logger
from infrastructure.utils.common.dictwrapper import DictWrapper
from support.common.generator.base import BaseGenerator
from support.common.generator.helper import SchoolGenerator, MajorGenerator

from abs.services.crm.university.models import Relations


class RelationsGenerator(BaseGenerator):


    def get_create_list(self, result_mapping):
        school_list = result_mapping.get(SchoolGenerator.get_key())
        major_list = result_mapping.get(MajorGenerator.get_key())
        relations_list = []
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
