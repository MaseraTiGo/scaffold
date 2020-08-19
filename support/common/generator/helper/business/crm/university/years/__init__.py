# coding=UTF-8


from infrastructure.log.base import logger
from infrastructure.utils.common.dictwrapper import DictWrapper
from support.common.generator.base import BaseGenerator
from support.common.generator.helper import RelationsGenerator

from abs.services.crm.university.models import Years


class YearsGenerator(BaseGenerator):

    def __init__(self, years_infos):
        super(YearsGenerator, self).__init__()
        self._years_infos = self.init(years_infos)

    def get_create_list(self, result_mapping):
        relations_list = result_mapping.get(RelationsGenerator.get_key())
        years_list = []
        for relations in relations_list:
            for years_info in self._years_infos:
                years_info.update({
                    "relations":relations,
                })
                years_list.append(DictWrapper(years_info))
        return years_list

    def create(self, years_info, result_mapping):
        years_qs = Years.query(
            relations = years_info.relations,
            category = years_info.category,
            duration = years_info.duration
        )
        if years_qs.count():
            years = years_qs[0]
        else:
            years = Years.create(**years_info)
        return years

    def delete(self):
        logger.info('================> delete years <==================')
        return None
