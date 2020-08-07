# coding=UTF-8


from infrastructure.core.exception.business_error import BusinessError
from infrastructure.utils.common.split_page import Splitor

from abs.common.manager import BaseManager
from abs.services.agent.goods.store.goods import Goods
from abs.middleground.business.merchandise.manager import MerchandiseServer
from abs.middleground.business.merchandise.utils.constant import UseStatus


class GoodsServer(BaseManager):

    @classmethod
    def search_goods(cls, current_page, **search_info):
        goods_qs = cls.search_all_goods(**search_info).order_by("-create_time")
        return Splitor(current_page, goods_qs)

    @classmethod
    def search_all_goods(cls, **search_info):
        merchandise_info = {}
        if 'title' in search_info:
            title = search_info.pop('title')
            merchandise_info.update({
                'title__contains': title
            })
        if 'use_status' in search_info:
            use_status = search_info.pop('use_status')
            merchandise_info.update({
                'use_status': use_status
            })
        if 'production_id' in search_info:
            production_id = search_info.pop('production_id')
            merchandise_info.update({
                'production_id': production_id
            })
        if merchandise_info:
            merchandise_id_list = MerchandiseServer.search_id_list(
                **merchandise_info
            )
            search_info.update({
                'merchandise_id__in': merchandise_id_list
            })
        return Goods.search(**search_info)

    @classmethod
    def search_enable_goods(cls, current_page, **search_info):
        search_info.update({'use_status': UseStatus.ENABLE})
        goods_qs = cls.search_all_goods(**search_info).order_by('-is_hot', "create_time")
        return Splitor(current_page, goods_qs)

    @classmethod
    def search_hot_goods(cls, **search_info):
        search_info.update({'use_status': UseStatus.ENABLE})
        return list(cls.search_all_goods(**search_info).order_by('-is_hot', "create_time")[0:3])

    @classmethod
    def get_goods(cls, goods_id):
        goods = Goods.get_byid(goods_id)
        if goods is None:
            raise BusinessError("此商品不存在")
        return goods

    @classmethod
    def update_goods(cls, goods, **update_info):
        goods.update(**update_info)
        return goods

    @classmethod
    def create_goods(cls, **goods_info):
        goods = Goods.create(**goods_info)
        return goods

    @classmethod
    def hung_goods(cls, merchandise_list):
        mapping = {}
        for merchandise in merchandise_list:
            merchandise.goods = None
            mapping.update({
                merchandise.id: merchandise
            })
        goods_list = Goods.search(merchandise_id__in = mapping.keys())
        for goods in goods_list:
            merchandise = mapping.get(goods.merchandise_id)
            merchandise.goods = goods
