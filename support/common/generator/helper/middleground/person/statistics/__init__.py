# coding=UTF-8


from infrastructure.log.base import logger
from infrastructure.utils.common.dictwrapper import DictWrapper
from support.common.generator.base import BaseGenerator
from support.common.generator.helper import PersonGenerator
from abs.middleground.business.person.store import PersonStatistics


class StatisticsGenerator(BaseGenerator):

    def get_create_list(self, result_mapping):
        person_list = result_mapping.get(PersonGenerator.get_key())
        statistics_list = []
        for person in person_list:
            statistics_info = DictWrapper({
                'person': person
            })
            statistics_list.append(statistics_info)
        return statistics_list

    def create(self, statistics_info, result_mapping):
        statistics_qs = PersonStatistics.query().filter(
            person=statistics_info.person
        )
        if statistics_qs.count():
            statistics = statistics_qs[0]
        else:
            statistics = PersonStatistics.create(**statistics_info)
        return statistics

    def delete(self):
        logger.info('===============>>> delete statistics <==================')
        return None
