# coding=UTF-8
import json
import random

from infrastructure.log.base import logger
from support.common.generator.base import BaseGenerator
from support.common.generator.field.normal import \
     AmountHelper
from support.common.generator.helper.middleground.merchandise import \
     MerchandiseGenerator
from support.common.generator.helper.middleground.production import \
     ProductionGenerator
from abs.middleground.business.merchandise.store import \
     Specification, SpecificationValue



class SpecificationGenerator(BaseGenerator):

    def get_create_list(self, result_mapping):
        merchandise_list = result_mapping.get(MerchandiseGenerator.get_key())
        production_list = result_mapping.get(ProductionGenerator.get_key())
        specification_list = []
        for merchandise in merchandise_list:
            production_fiter = list(filter(
                lambda obj: obj.id == merchandise.production_id,
                production_list
            ))

            if production_fiter:
                production = production_fiter[0]
                attribute_list = json.loads(production.attribute_list)
                specification_infos = {
                    "show_image":"",
                    "sale_price":AmountHelper().generate(),
                    "stock":AmountHelper().generate(),
                    "merchandise":merchandise,
                    "remark":"这个是一个规格备注",
                    "value_list":[{
                       "category":attribute_list[0]["category"],
                       "attribute":random.choice(
                            attribute_list[0]["attribute_list"]
                        )["name"]
                    }]
                }
                specification_list.append(specification_infos)
        return specification_list

    def create(self, specification_info, result_mapping):
        value_list = specification_info.pop("value_list")
        specification = Specification.create(**specification_info)
        for value in value_list:
            SpecificationValue.create(**{
                "category":value["category"],
                "attribute":value["attribute"],
                "specification":specification
            })
        return specification

    def delete(self):
        logger.info('================> delete specification <==================')
        return None
