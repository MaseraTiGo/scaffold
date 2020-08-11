# coding=UTF-8
import random

from support.common.generator.base import BaseGenerator
from support.common.generator.helper.middleground.merchandise import \
        MerchandiseGenerator
from support.common.generator.helper.business.crm.university.major import \
        MajorGenerator
from support.common.generator.helper.business.crm.university.school import \
        SchoolGenerator
from support.common.generator.helper.business.crm.agent import \
        AgentGenerator
from abs.services.agent.goods.models import Goods


class GoodsGenerator(BaseGenerator):

    def __init__(self, goods_info):
        super(GoodsGenerator, self).__init__()
        self._goods_info = self.init(goods_info)

    def get_create_list(self, result_mapping):
        merchandise_list = result_mapping.get(MerchandiseGenerator.get_key())
        major_list = result_mapping.get(MajorGenerator.get_key())
        school_list = result_mapping.get(SchoolGenerator.get_key())
        agent_list = result_mapping.get(AgentGenerator.get_key())
        goods_list = []
        for goods_info in self._goods_info:
            merchandise = random.choice(merchandise_list)
            major = random.choice(major_list)
            school = random.choice(school_list)
            agent = random.choice(agent_list)
            goods_info.update({
                "school_id":school.id,
                "major_id":major.id,
                "merchandise_id":merchandise.id,
                "agent_id":agent.id,
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
