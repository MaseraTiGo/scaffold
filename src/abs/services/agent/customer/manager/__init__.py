# coding=UTF-8
import datetime

from infrastructure.core.exception.business_error import BusinessError
from infrastructure.utils.common.split_page import Splitor

from abs.common.manager import BaseManager
from abs.services.agent.customer.store.salechance import SaleChanceOrder
from abs.middleground.business.person.manager import PersonServer
from abs.services.agent.customer.models import AgentCustomer, \
     AgentCustomerSaleChance


class AgentCustomerServer(BaseManager):

    @classmethod
    def create(cls, **info):
        result, agent_customer = cls.is_exist(
            info["agent_id"],
            info["phone"]
        )
        if result:
            return agent_customer
        return AgentCustomer.create(**info)

    @classmethod
    def is_exist(cls, agent_id, phone):
        agent_customer_qs = cls.search_all(
            agent_id = agent_id,
            phone = phone
        )
        if agent_customer_qs.count() > 0:
            return True, agent_customer_qs[0]
        return False, None

    @classmethod
    def get(cls, agent_customer_id):
        agent_customer = AgentCustomer.get_byid(
            agent_customer_id
        )
        if agent_customer is None:
            raise BusinessError("此客户不存在")
        return agent_customer

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
        PersonServer.hung_persons(splitor.get_list())
        return splitor

    @classmethod
    def create_foradd_order(cls, customer, agent_id, order_id):
        person = PersonServer.get(customer.person_id)
        agent_customer = AgentCustomer.search(
            phone = person.phone,
            agent_id = agent_id
        ).first()
        if agent_customer:
            agent_customer.update(
                person_id = person.id
            )
        else:
            AgentCustomer.create(
                agent_id = agent_id,
                person_id = person.id,
                phone = person.phone,
                name = person.name,
            )
        sale_chance = AgentCustomerSaleChance.search(
            agent_customer = agent_customer,
            end_time__gt = datetime.date.today()
        ).first()
        if sale_chance:
            SaleChanceOrder.create(
                sale_chance = sale_chance,
                order_id = order_id
            )
        return agent_customer

    @classmethod
    def check_byphone(cls, phone, agent_id):
        agent_customer_qs = cls.search_all(
            phone = phone,
            agent_id = agent_id
        )
        if agent_customer_qs.count() > 0:
            return agent_customer_qs[0]
        else:
            return None

    @classmethod
    def hung_agent_customer(cls, obj_list):
        agent_customer_mapping = {}
        for obj in obj_list:
            obj.agent_customer = None
            if obj.agent_customer_id not in agent_customer_mapping:
                agent_customer_mapping[obj.agent_customer_id] = []
            agent_customer_mapping[obj.agent_customer_id].append(obj)
        agent_customer_list = list(
            AgentCustomer.search(id__in = agent_customer_mapping.keys())
        )
        PersonServer.hung_persons(agent_customer_list)
        for agent_customer in agent_customer_list:
            if agent_customer.id in agent_customer_mapping:
                for obj in agent_customer_mapping[agent_customer.id]:
                    obj.agent_customer = agent_customer
        return obj_list


class SaleChanceServer(BaseManager):

    @classmethod
    def create(cls, **sale_chance_info):
        sale_chance = AgentCustomerSaleChance.create(**sale_chance_info)
        return sale_chance

    @classmethod
    def search(cls, current_page, **search_info):
        search_info.update({
            "end_time__gt":datetime.date.today()
        })
        sale_chance_qs = cls.search_all(
            **search_info
        ).order_by("-create_time")
        splitor = Splitor(current_page, sale_chance_qs)
        return splitor

    @classmethod
    def search_all(cls, **search_info):
        if "name" in search_info:
            name = search_info.pop("name")
            search_info.update({"agent_customer__name":name})
        if "phone" in search_info:
            phone = search_info.pop("phone")
            search_info.update({"agent_customer__phone":phone})
        sale_chance_qs = AgentCustomerSaleChance.search(**search_info)
        return sale_chance_qs

    @classmethod
    def is_exist(cls, agent_customer):
        sale_chance = cls.search_all(
            agent_customer = agent_customer,
            end_time__gt = datetime.date.today()
        )
        if sale_chance.count() > 0:
            return True
        return False
