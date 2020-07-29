# coding=UTF-8


from infrastructure.core.exception.business_error import BusinessError
from infrastructure.utils.common.split_page import Splitor

from abs.common.manager import BaseManager
from abs.services.crm.production.store.goods import Goods


class GoodsServer(BaseManager):

    @classmethod
    def search_goods(cls, current_page, **search_info):
        goods_qs =cls.search_all_goods(**search_info)
        return Splitor(current_page, goods_qs)

    @classmethod
    def search_all_goods(cls, **search_info):
        return Goods.search(**search_info)
