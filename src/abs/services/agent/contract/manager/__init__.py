# coding=UTF-8


from infrastructure.core.exception.business_error import BusinessError
from infrastructure.utils.common.split_page import Splitor

from abs.common.manager import BaseManager


class ContractServer(BaseManager):

    @classmethod
    def create(cls, **search_info):
        pass
