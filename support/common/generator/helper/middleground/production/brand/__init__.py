# coding=UTF-8


from infrastructure.log.base import logger
from infrastructure.utils.common.dictwrapper import DictWrapper
from support.common.generator.base import BaseGenerator
from support.common.generator.helper.middleground.enterprise import \
        EnterpriseGenerator
from abs.middleground.business.production.store import Brand


class BrandGenerator(BaseGenerator):

    def __init__(self, brand_infos):
        super(BrandGenerator, self).__init__()
        self._brand_infos = self.init(brand_infos)

    def get_create_list(self, result_mapping):
        enterprise_list = result_mapping.get(EnterpriseGenerator.get_key())
        brand_list = []
        for enterprise in enterprise_list:
            for brand_info in self._brand_infos:
                brand = brand_info.copy()
                brand.update({
                    'company_id': enterprise.id
                })
                brand_list.append(DictWrapper(brand))
        return brand_list

    def create(self, brand_info, result_mapping):
        brand_qs = Brand.query(
            company_id=brand_info.company_id,
            name=brand_info.name,
        )
        if brand_qs.count():
            brand = brand_qs[0]
        else:
            brand = Brand.create(**brand_info)
        return brand

    def delete(self):
        logger.info('================> delete customer <==================')
        return None
