# coding=UTF-8

from abs.common.manager import BaseManager
from abs.services.customer.personal.store.message import CustomerMessage
from infrastructure.utils.common.split_page import Splitor


class CustomerMessageServer(BaseManager):

    @classmethod
    def search(cls, current_page, **search_info):
        customer_qs = CustomerMessage.search(**search_info).order_by('-create_time')
        customer_qs_split = Splitor(current_page, customer_qs)
        return customer_qs_split

    @classmethod
    def update(cls, message_id, **update_info):
        message_obj = CustomerMessage.get_byid(message_id)
        message_obj.update(**update_info)
        return message_obj

    @classmethod
    def count_unread(cls, **search_info):
        return CustomerMessage.search(**search_info).count()
