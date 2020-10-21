# coding=UTF-8

import random
import time
import datetime
from support.common.generator.field.model.constant import GenderConstant
from support.common.maker import BaseLoader


class CustomerOrderLoader(BaseLoader):
    source_list = ['app', 'crm', 'wechat', 'other']
    status_list = ["order_launched", "payment_finished",
                   "delivery_finished", "order_closed",
                   "order_finished"]
    pay_service_method = ['full_payment', 'installment']

    def generate(self):
        return [{
            'deposit': random.randint(0, 100),
            # 'agent_customer_id': agent_customer.id,
            # 'mg_order_id': mg_order.id,
            # 'agent_id': agent_customer.agent_id,
            # 'person_id': agent_customer.person_id,
            # 'company_id': agent_customer.agent.company_id,
            'source': random.choice(self.source_list),
            'number': 'OD-' + str(time.time()).replace('.', ''),
            'status': random.choice(self.status_list),
            # 'name': invoice_info.get('name'),
            # 'phone': invoice_info.get('phone'),
            'pay_services': random.choice(self.pay_service_method)
        }]
