# coding=UTF-8
import random
from support.common.generator.field.normal import \
        AmountHelper
from support.common.generator.field.model import \
        DespatchServiceConstant, UseStatusConstant, DurationTypesConstant
from support.common.maker import BaseLoader


class GoodsLoader(BaseLoader):

    def generate(self):
        times = random.randint(3, 10)
        goods_list = []
        for _ in range(times):
            title = "这是一个商品" + str(random.randint(0, 100)).rjust(3, '0')
            goods = {
                'title': title,
                'description': "这是一个商品描述",
                'slideshow': "[]",
                'video_display': "",
                'detail': "[]",
                'market_price': AmountHelper().generate(),
                'pay_types': '[]',
                'pay_services': '[]',
                'despatch_type': DespatchServiceConstant().generate(),
                'use_status': UseStatusConstant().generate(),
                'remark': "这是一个备注",
                'duration': DurationTypesConstant().generate(),
            }
            goods_list.append(goods)
        return goods_list
