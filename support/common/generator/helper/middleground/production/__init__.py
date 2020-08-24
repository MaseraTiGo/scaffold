# coding=UTF-8


from infrastructure.log.base import logger
from support.common.generator.base import BaseGenerator
from support.common.generator.helper.middleground.production.brand import \
        BrandGenerator
from abs.middleground.business.production.store import Production


class ProductionGenerator(BaseGenerator):

    def __init__(self, production_infos):
        super(ProductionGenerator, self).__init__()
        self._production_infos = self.init(production_infos)

    def get_create_list(self, result_mapping):
        brand_list = result_mapping.get(BrandGenerator.get_key())
        production_list = []
        for production_info in self._production_infos:
            brand_fiter = list(filter(
                lambda obj: obj.name == production_info.brand_name,
                brand_list
            ))
            if brand_fiter:
                brand = brand_fiter[0]
                production_info.update({
                    'brand': brand,
                    'company_id': brand.company_id,
                })
                production_list.append(production_info)
        return production_list

    def create(self, production_info, result_mapping):
        production_qs = Production.query(
            company_id = production_info.company_id,
            name = production_info.name,
            brand = production_info.brand,
        )
        if production_qs.count():
            production = production_qs[0]
        else:
            production = Production.create(**production_info)
        return production

    def delete(self):
        logger.info('==============>>> delete production <=================')
        return None
