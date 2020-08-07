# coding=UTF-8


from infrastructure.core.exception.business_error import BusinessError
from infrastructure.utils.common.split_page import Splitor

from abs.common.manager import BaseManager
from abs.services.agent.customer.models import AgentCustomer


class AgentStaffServer(BaseManager):

    @classmethod
    def create(cls, **info):
        return AgentCustomer.create(**info)
