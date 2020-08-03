# coding=UTF-8
import random

from infrastructure.log.base import logger
from support.common.generator.base import BaseGenerator
from abs.middleground.business.merchandise.store import Merchandise
from support.common.generator.helper.middleground.production import \
        ProductionGenerator


class MerchandiseGenerator(BaseGenerator):

    def __init__(self, merchandise_infos):
        super(MerchandiseGenerator, self).__init__()
        self._merchandise_infos = self.init(merchandise_infos)

    def get_create_list(self, result_mapping):
        production_list = result_mapping.get(ProductionGenerator.get_key())
        merchandise_list = []
        for merchandise_infos in self._merchandise_infos:
            production = random.choice(production_list)
            merchandise_infos.update({
                "company_id":production.company_id,
                "production_id":production.id,
            })
            merchandise_list.append(merchandise_infos)
        return merchandise_list

    def create(self, merchandise_info, result_mapping):
        merchandise_qs = Merchandise.query().filter(
            title=merchandise_info.title,
            company_id=merchandise_info.company_id,
        )
        if merchandise_qs.count():
            merchandise = merchandise_qs[0]
        else:
            merchandise = Merchandise.create(**merchandise_info)
        return merchandise

    def delete(self):
        logger.info('=================>>> delete merchandise <=================')
        return None
