# coding=UTF-8
import random

from abs.services.agent.goods.store.goods import GoodsReview
from abs.services.agent.account.store.account import StaffAccount
from support.common.generator.base import BaseGenerator
from support.common.generator.helper.business.agent.goods import GoodsGenerator


class GoodsReviewGenerator(BaseGenerator):

    # def __init__(self, goods_review_info):
    #     super(GoodsReviewGenerator, self).__init__()
    #     self._goods_review_info = self.init(goods_review_info)

    def get_create_list(self, result_mapping):
        goods_list = result_mapping.get(GoodsGenerator.get_key())
        sa_qs = StaffAccount.objects.all()
        goods_review_list = []
        for goods in goods_list:
            goods_review_info = {}
            goods_review_info.update({
                'staff_id': random.choice(sa_qs).id,
                'goods': goods,
                'status': random.choice(['wait_review'])
            })
            goods_review_list.append(goods_review_info)
        return goods_review_list

    def create(self, goods_review_info, result_mapping):
        goods_qs = GoodsReview.search(goods=goods_review_info['goods'])
        if goods_qs.count() > 0:
            return goods_qs[0]
        else:
            goods_review = GoodsReview.create(
                **goods_review_info
            )
            return goods_review

    def delete(self):
        print('===================>>> delete goods review<====================')
        return None
