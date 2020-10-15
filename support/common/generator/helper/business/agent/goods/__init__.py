# coding=UTF-8
import random

from support.common.generator.base import BaseGenerator
from support.common.generator.helper.middleground.merchandise import \
        MerchandiseGenerator
from support.common.generator.helper.business.crm.university.years import \
        YearsGenerator
from support.common.generator.helper.business.crm.agent import \
        AgentGenerator
from abs.services.agent.goods.models import Goods
from support.common.generator.helper.business.agent.template import TemplateGenerator
from abs.middleground.business.production.store import Production


class GoodsGenerator(BaseGenerator):

    def __init__(self, goods_info):
        super(GoodsGenerator, self).__init__()
        self._goods_info = self.init(goods_info)

    def get_relative_year(self, result_mapping, production_name):
        category_mapping = {
            '专升本': 'UNDERGRADUATE',
            '高起专': 'SPECIALTY',
            '高起本': 'HIGHCOST',
            '考研': 'GRADUATE',
            '资格证': 'QUALIFICATION',
            '其它': 'OTHER'
        }
        category = category_mapping.get(production_name, 'specialty')
        years_list = result_mapping.get(YearsGenerator.get_key())
        years = [year for year in years_list if year.category == category.lower()][0]
        return years

    def get_create_list(self, result_mapping):
        merchandise_list = result_mapping.get(MerchandiseGenerator.get_key())
        template_list = result_mapping.get(TemplateGenerator.get_key())
        years_list = result_mapping.get(YearsGenerator.get_key())
        agent_list = result_mapping.get(AgentGenerator.get_key())
        goods_list = []
        for goods_info in self._goods_info:
            merchandise = random.choice(merchandise_list)
            production_id = merchandise.production_id
            production_name = Production.search(id=production_id)[0].name
            years = self.get_relative_year(result_mapping, production_name)
            template = random.choice(template_list)
            agent = random.choice(agent_list)
            goods_info.update({
                "school_id":years.relations.school.id,
                "major_id":years.relations.major.id,
                "merchandise_id":merchandise.id,
                "agent_id":agent.id,
                "relations_id":years.relations.id,
                "years_id":years.id,
                "template_id": template.id,
            })
            goods_list.append(goods_info)
        return goods_list

    def create(self, goods_info, result_mapping):
        goods_qs = Goods.search(merchandise_id = goods_info.merchandise_id)
        if goods_qs.count() > 0:
            return goods_qs[0]
        else:
            goods = Goods.create(
                **goods_info
            )
            return goods

    def delete(self):
        print('===================>>> delete goods <====================')
        return None
