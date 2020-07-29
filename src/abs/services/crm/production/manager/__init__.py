# coding=UTF-8


from infrastructure.core.exception.business_error import BusinessError
from infrastructure.utils.common.split_page import Splitor

from abs.common.manager import BaseManager


class GoodsServer(BaseManager):

    @classmethod
    def search(cls, current_page, **search_info):
        pass
