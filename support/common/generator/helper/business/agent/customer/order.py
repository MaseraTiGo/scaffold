# coding=UTF-8

import random
from support.common.generator.base import BaseGenerator
from abs.middleground.business.person.models import Person,\
        PersonStatus, PersonStatistics
from abs.services.agent.order.store import Order
from abs.services.agent.order.store import OrderItem
from abs.middleground.business.order.store.entity.order import Order as MgOrder
from abs.middleground.business.order.store.entity.payment import Payment
from abs.middleground.business.order.store.entity.requirement import Requirement
from abs.middleground.business.order.store.entity.invoice import Invoice
from support.common.generator.helper.business.agent.customer import CustomerGenerator
# from support.common.generator.helper.business.agent.goods import GoodsGenerator
from support.common.generator.helper.business.crm.agent import AgentGenerator


class OrderGenerator(BaseGenerator):
    """
    deprecated:
    through creating new goods. the whole process will be walked by.
    """

    # todo: not obey the norm, need to be modified.

    # def __init__(self, order_info):
    #     super(OrderGenerator, self).__init__()
    #     self._order_infos = self.init(order_info)
    #
    # def get_requirement_obj(self):
    #     return Requirement.create(sale_price=random.randint(10000, 99999))
    #
    # def get_payment_obj(self):
    #     return Payment.create(actual_amount=random.randint(1000, 9999))
    #
    # def get_invoice_obj(self, name, phone, requirement):
    #     return Invoice.create(**{
    #         'name': name,
    #         'phone': phone,
    #         'requirement': requirement
    #     })
    #
    # def get_mg_order(self, requirement, payment, invoice, l_id, s_id):
    #     create_info = {
    #         'number': MgOrder.generate_number(),
    #         'strike_price': random.randint(10000, 99999),
    #         'requirement': requirement,
    #         'payment': payment,
    #         'invoice': invoice,
    #         'launch_type': random.choice(['company', 'person']),
    #         'server_type': random.choice(['company', 'person']),
    #         'launch_id': l_id,
    #         'server_id': s_id
    #     }
    #     return MgOrder.create(**create_info)
    #
    # def set_order_item(self):
    #     # todo: need to be completed.
    #     order_item_info = {
    #         'goods_id': 1,
    #         'merchandise_snapshoot_id': 1,
    #         'school_name': '武汉理工大学',
    #         'school_city': '武汉市',
    #         'marjor_name': '电子信息工程',
    #         'category': 'other',
    #         'duration': 'two_half_year',
    #         'order_id': 1,
    #         'template_id': 1,
    #         'evaluation': 'wait_evaluation'
    #     }
    #     OrderItem.create(**order_item_info)
    #
    # def set_snapshoot(self):
    #     # todo: need to be completed.
    #     snapshoot_info = {
    #         'production_id': 1,
    #         'merchandise_id': 1,
    #         'specification_id': 1,
    #         'title': '生活当如此',
    #         'sale_price': 0,
    #         'count': 1,
    #         'total_price': 3000,
    #         'requirement_id': 1,
    #         'brand_name': '成教',
    #         'production_name': '专升本',
    #         'despatch_type': 'eduction_contract',
    #     }
    #
    #
    # def get_create_list(self, result_mapping):
    #     requirement = self.get_requirement_obj()
    #     payment = self.get_payment_obj()
    #
    #     customers = result_mapping.get(CustomerGenerator.get_key())
    #     agents = result_mapping.get(AgentGenerator.get_key())
    #     for order_info in self._order_infos:
    #         customer = random.choice(customers)
    #         invoice = self.get_invoice_obj(customer.name, customer.phone, requirement)
    #         mg_order = self.get_mg_order(requirement, payment, invoice, customer.id, customer.agent_id)
    #         agent = random.choice(agents)
    #         temp_dict = {
    #             'name': customer.name,
    #             'phone': customer.phone,
    #             'agent_id': customer.agent_id,
    #             'person_id': 5,
    #             'agent_customer_id': customer.id,
    #             'mg_order_id': mg_order.id,
    #             'number': mg_order.number,
    #             'company_id': agent.company_id,
    #         }
    #         order_info.update(temp_dict)
    #     return self._order_infos
    #
    # def create(self, order_info, result_mapping):
    #
    #     order_qs = Order.search(number=order_info['number'])
    #     if order_qs.count() > 0:
    #         return order_qs[0]
    #     else:
    #         order = Order.create(
    #             **order_info
    #         )
    #         return order
    #
    # def delete(self):
    #     print('===================>>> delete order <====================')
    #     return None
