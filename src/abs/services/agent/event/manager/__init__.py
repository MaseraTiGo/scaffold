# coding=UTF-8
import datetime

from infrastructure.core.exception.business_error import BusinessError
from infrastructure.utils.common.split_page import Splitor

from abs.common.manager import BaseManager

from abs.services.agent.event.models import OperationEvent, StaffOrderEvent


class OperationEventServer(BaseManager):

    @classmethod
    def create(cls, **info):
        operation = OperationEvent.create(**info)
        return operation

    @classmethod
    def search(cls, current_page, **search_info):
        operation_qs = cls.search_all(**search_info).\
                   order_by("-create_time")
        splitor = Splitor(current_page, operation_qs)
        return splitor

    @classmethod
    def search_all(cls, **search_info):
        operation_qs = OperationEvent.search(**search_info)
        return operation_qs


class StaffOrderEventServer(BaseManager):

    @classmethod
    def create(cls, **info):
        event = StaffOrderEvent.create(**info)
        return event

    @classmethod
    def get_order_ids(cls, **search_info):
        order_ids = StaffOrderEvent.search(**search_info).values_list(
            'order_id',
            flat = True
        )
        return order_ids