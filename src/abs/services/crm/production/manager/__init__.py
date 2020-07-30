# coding=UTF-8


from infrastructure.core.exception.business_error import BusinessError
from infrastructure.utils.common.split_page import Splitor

from abs.common.manager import BaseManager
from abs.services.crm.production.store.goods import Goods
from abs.middleground.business.production.manager import ProductionServer
from abs.middleground.business.merchandise.manager import MerchandiseServer
from abs.services.crm.university.manager import UniversityServer


class GoodsServer(BaseManager):

    @classmethod
    def search_goods(cls, current_page, **search_info):
        goods_qs = cls.search_all_goods(**search_info)
        page_list = Splitor(current_page, goods_qs)
        UniversityServer.hung_major(page_list.data)
        UniversityServer.hung_school(page_list.data)
        MerchandiseServer.hung_merchandise(page_list.data)
        merchandise_list = [goods.merchandise for goods in page_list.data]
        ProductionServer.hung_production(merchandise_list)
        return page_list

    @classmethod
    def search_all_goods(cls, **search_info):
        return Goods.search(**search_info)
