# coding=UTF-8


from infrastructure.core.exception.business_error import BusinessError
from infrastructure.utils.common.split_page import Splitor

from abs.common.manager import BaseManager
from abs.services.agent.customer.models import AgentCustomer


class AgentCustomerServer(BaseManager):

    @classmethod
    def create(cls, **info):
        result, agent_customer = cls.is_exist(
            info["agent_id"],
            info["customer_id"]
        )
        if result:
            return agent_customer
        return AgentCustomer.create(**info)

    @classmethod
    def is_exist(cls, agent_id, customer_id):
        agent_customer_qs = cls.search_all(
            agent_id = agent_id,
            customer_id = customer_id
        )
        if agent_customer_qs.count() > 0:
            return True, agent_customer_qs[0]
        return False, None


    @classmethod
    def search_all(cls, **search_info):
        agent_customer_qs = AgentCustomer.search(
            **search_info
        )
        return agent_customer_qs

    @classmethod
    def search(cls, current_page, **search_info):
        agent_customer_qs = cls.search_all(
            **search_info
        ).order_by("-create_time")
        splitor = Splitor(current_page, agent_customer_qs)
        return splitor